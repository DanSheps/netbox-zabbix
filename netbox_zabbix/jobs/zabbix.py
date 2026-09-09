import logging

from django.db.models import Q
from zabbix_utils import ZabbixAPI

from django.db import models

from dcim.models import Device, VirtualDeviceContext, VirtualChassis
from ipam.models import IPAddress
from netbox.context_managers import event_tracking
from netbox.jobs import JobRunner, system_job
from netbox_zabbix.choices import (
    ZabbixHostInterfaceTypeChoices,
    ZabbixHostInterfaceConnectionChoices,
)
from netbox_zabbix.jobs.mixins import JobInstanceMixin
from netbox_zabbix.models import *
from netbox_zabbix.utilities import has_changes

__all__ = ('SystemSyncZabbixHostGroups',)

from virtualization.models import VirtualMachine

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


class SyncZabbixSyncMixin:
    def get_fields(self, model):
        for field in model._meta.fields:
            if field.name in [
                'id',
                'created',
                'last_updated',
                'local_context_data',
                'custom_field_data',
                'comments',
                'zid',
            ]:
                continue
            elif type(field) not in [models.ForeignKey, models.ManyToManyField]:
                yield field.name

    def process_model_fields(self, instance, entry):
        fields = self.get_fields(instance)
        for field in list(fields):
            if field == 'description' and entry.get(field):
                if len(entry.get(field)) > 200:
                    setattr(instance, field, entry.get(field)[0:200])
                    instance.comment = entry.get(field)
                else:
                    setattr(instance, field, entry.get(field))
            elif entry.get(field):
                setattr(instance, field, entry.get(field))

        return instance

    def process_m2m_fields(self, instance, entry):
        return

    def process_fields(self, instance, entry):
        instance = self.process_model_fields(instance, entry)
        return instance

    def sync(self, model=None, servers=None, once=False):
        entry = None
        try:
            self.logger.debug(f"Syncing {model.__name__} objects")
            instance = self.get_instance()
            if not model:
                raise Exception('No model specified')
            elif instance:
                servers = [server for server in instance.servers.all()]
                model = type(instance)
                model_name = model.get_api_name()
                key_field = model.get_zid_field_name()
                name_field = model.get_name_field_name()
            else:
                model_name = model.get_api_name()
                key_field = model.get_zid_field_name()
                name_field = model.get_name_field_name()
                if not servers:
                    servers = ZabbixServer.objects.all()

            for server in servers:
                try:
                    zabbix = ZabbixAPI(
                        url=server.api_url,
                        token=server.api_token,
                        validate_certs=server.validate_certificates,
                    )
                    self.logger.debug(f"Connected to {server}")
                except Exception as e:
                    logger.error(
                        f"Failed to connect to Zabbix server {server.name}: {e}"
                    )
                    self.logger.error(
                        f"Failed to connect to Zabbix server {server.name}: {e}"
                    )
                    continue

                if not instance:
                    objects = getattr(zabbix, model_name).get(model.get_query_flags())
                else:
                    objects = [
                        getattr(zabbix, model_name).get(
                            **{key_field: instance.zid, **model.get_query_flags()}
                        )
                    ]

                pks = []
                for entry in objects:
                    self.logger.debug(f"Processing {entry[key_field]}")
                    # self.logger.debug(f"Entry: {entry}")
                    try:
                        filter = Q()
                        filter |= Q(zid=entry[key_field])
                        # self.logger.info(f"Model Has 'name': {hasattr(model, 'name')}")
                        # self.logger.info(f"Model Has 'assigned_object': {hasattr(model, 'assigned_object')}")
                        # self.logger.info(f"Entry has '{name_field}': {entry.get(name_field)}")
                        if hasattr(model, 'name') and entry.get(name_field):
                            filter |= Q(name=entry.get(name_field))
                        elif hasattr(model, 'assigned_object') and entry.get(
                            name_field
                        ):
                            filter |= Q(devices__name=entry.get(name_field))
                            filter |= Q(vdcs__name=entry.get(name_field))
                            filter |= Q(virtual_machines__name=entry.get(name_field))
                            filter |= Q(virtual_chassis__name=entry.get(name_field))
                        qp = model.get_additional_filter_query_params(server, entry)
                        item = model.objects.filter(filter, **qp).distinct().get()

                        self.logger.info(f"Found instance: {item}")
                        item.snapshot()
                        if item.zid is None:
                            item.zid = entry[key_field]
                        item = self.process_fields(item, entry)
                        if has_changes(item):
                            item.full_clean()
                            item.save()
                            self.logger.info(f'{item} has changes and has been saved')
                        self.process_m2m_fields(item, entry)
                        pks.append(item.pk)
                    except model.DoesNotExist:
                        item = model.instantiate(server, entry, key_field)
                        if not item:
                            # self.logger.info(f'{entry.get(key_field)} is skipped as zabbix host is not found')
                            continue
                        item = self.process_fields(item, entry)
                        if item is not None:
                            item.full_clean()
                            item.save()
                            pks.append(item.pk)
                            self.process_m2m_fields(item, entry)
                            self.logger.info(f'{item} is new and has been saved')
                        else:
                            self.logger.info(
                                f'{entry.get(key_field)} is skipped as device, vm or vdc is not found'
                            )
                    if once:
                        import pprint

                        pprint.pprint(entry)
                        return

                if model.objects.exclude(pk__in=pks).exists():
                    model.objects.exclude(pk__in=pks).delete()
        except Exception as e:
            import traceback

            self.logger.error(f"Failed to sync {model.__name__} objects: {e}")
            self.logger.error(f'{traceback.format_exc()}')
            self.logger.error(f'{entry}')
            raise e


class SyncZabbixHostMixin:
    def process_fields(self, instance, entry):
        if instance.assigned_object is None:
            filter = Q()
            filter |= Q(name=entry.get('host'))
            filter |= Q(custom_field_data__zabbix_hostid=entry.get('hostid'))

            host = None
            device = Device.objects.filter(filter)
            virtual_machine = VirtualMachine.objects.filter(filter)
            vdc = VirtualDeviceContext.objects.filter(filter)
            vc = VirtualChassis.objects.filter(filter)
            if device.exists():
                host = device.first()
            elif vdc.exists():
                host = vdc.first()
            elif vc.exists():
                host = vc.first()
            elif virtual_machine.exists():
                host = virtual_machine.first()
            else:
                self.logger.error(f"Failed to find host for {entry.get('name')}")
                return None

            self.logger.info(f"Located host for {host} :: {entry.get('name')}")
            instance = self.process_model_fields(instance, entry)
            instance.assigned_object = host
        else:
            instance = self.process_model_fields(instance, entry)
        return instance

    def process_m2m_fields(self, instance, entry):
        group_ids = [group.get('groupid') for group in entry.get('hostgroups', [])]
        template_ids = [
            template.get('templateid') for template in entry.get('parentTemplates', [])
        ]

        groups = ZabbixHostGroup.objects.filter(zid__in=group_ids)
        templates = ZabbixTemplate.objects.filter(zid__in=template_ids)

        instance.groups.set(groups)
        instance.templates.set(templates)


@system_job(interval=1440)
class SystemSyncZabbixProxyGroups(SyncZabbixSyncMixin, JobInstanceMixin, JobRunner):
    def run(self, data=None, commit=True, *args, **kwargs):
        with event_tracking(request=None):
            self.sync(model=ZabbixProxyGroup)


@system_job(interval=1440)
class SystemSyncZabbixProxies(SyncZabbixSyncMixin, JobInstanceMixin, JobRunner):
    def run(self, data=None, commit=True, *args, **kwargs):
        with event_tracking(request=None):
            self.sync(model=ZabbixProxy)


@system_job(interval=1440)
class SystemSyncZabbixHostGroups(SyncZabbixSyncMixin, JobInstanceMixin, JobRunner):
    def run(self, data=None, commit=True, *args, **kwargs):
        with event_tracking(request=None):
            self.sync(model=ZabbixHostGroup)


@system_job(interval=1440)
class SystemSyncZabbixTemplates(SyncZabbixSyncMixin, JobInstanceMixin, JobRunner):
    def run(self, data=None, commit=True, *args, **kwargs):
        with event_tracking(request=None):
            self.sync(model=ZabbixTemplate)


@system_job(interval=1440)
class SystemSyncZabbixHost(
    SyncZabbixHostMixin, SyncZabbixSyncMixin, JobInstanceMixin, JobRunner
):

    def run(self, data=None, commit=True, *args, **kwargs):
        with event_tracking(request=None):
            self.sync(model=ZabbixHost)


@system_job(interval=1440)
class SystemSyncZabbixHostInterface(SyncZabbixSyncMixin, JobInstanceMixin, JobRunner):

    def process_fields(self, instance, entry):
        instance = self.process_model_fields(instance, entry)
        instance.type = ZabbixHostInterfaceTypeChoices.MAPPING.get(entry.get('type'))
        instance.connection = (
            ZabbixHostInterfaceConnectionChoices.IP
            if entry.get('useip')
            else ZabbixHostInterfaceConnectionChoices.DNS
        )

        if ip := entry.get('ip'):
            try:
                instance.ip = IPAddress.objects.get(address__startswith=f'{ip}/')
            except IPAddress.DoesNotExist:
                instance.ip = IPAddress(address=f'{ip}/24')
                instance.ip.full_clean()
                instance.ip.save()
            except IPAddress.MultipleObjectsReturned:
                self.logger.info(f'Multiple IPs found for {ip}')

        return instance

    def process_m2m_fields(self, instance, entry):
        if instance.type == ZabbixHostInterfaceTypeChoices.SNMP:
            try:
                snmp = ZabbixHostInterfaceSNMP.objects.get(interface=instance)
                snmp.snapshot()
            except ZabbixHostInterfaceSNMP.DoesNotExist:
                snmp = ZabbixHostInterfaceSNMP(interface=instance)

            snmp = super().process_fields(snmp, entry.get('details'))

            if has_changes(snmp):
                snmp.full_clean()
                snmp.save()

    def run(self, data=None, commit=True, *args, **kwargs):
        with event_tracking(request=None):
            self.sync(model=ZabbixHostInterface)
