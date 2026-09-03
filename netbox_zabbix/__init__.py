from django.utils.translation import gettext as _

from netbox.plugins import PluginConfig
from importlib.metadata import metadata

metadata = metadata('netbox_zabbix')


class ZabbixPlugin(PluginConfig):
    name = metadata.get('Name').replace('-', '_')
    verbose_name = metadata.get('Summary')
    description = metadata.get('Description')
    version = metadata.get('Version')
    author = metadata.get('Author')
    author_email = metadata.get('Author-email')
    base_url = 'zabbix'
    min_version = '4.5.0'
    required_settings = [
        'username',
        'password',
    ]
    default_settings = {
        'tags': ['automation: monitoring'],
        'snmp': {
            'version': '2c',  # 1, 2c, 3
            'community': None,
            'context': None,
            'username': None,
            'level': None,  # None, noAuthNoPriv, authNoPriv, authPriv
            'auth_protocol': None,  # None, MD5, SHA1, SHA224, SHA256, SHA384, SHA512
            'auth_passphrase': None,
            'priv_protocol': None,  # None, DES, AES128, AES192, AES256, AES192C, AES256C
            'priv_passphrase': None,
        },
    }
    queues = []
    validated_config = None
    django_apps = []

    def ready(self):
        super().ready()
        try:
            from netbox_zabbix.jobs.zabbix import SystemSyncZabbixHostGroups
        except ImportError:
            pass

        try:
            from netbox_zabbix.signals.change_logging import (
                handle_changed_object_special,
            )
        except ImportError:
            print("No extended change logging")

        try:
            from django.contrib.contenttypes.fields import GenericRelation
            from netbox_zabbix.models.zabbix.host import ZabbixHost
            from dcim.models import Device, VirtualDeviceContext, VirtualChassis
            from virtualization.models import VirtualMachine

            GenericRelation(
                verbose_name=_('Zabbix Host Assignment'),
                to=ZabbixHost,
                related_name='devices',
                related_query_name='devices',
                content_type_field='assigned_object_type',
                object_id_field='assigned_object_id',
            ).contribute_to_class(Device, 'zabbix_hosts')

            GenericRelation(
                verbose_name=_('Zabbix Host Assignment'),
                to=ZabbixHost,
                related_name='vdcs',
                related_query_name='vdcs',
                content_type_field='assigned_object_type',
                object_id_field='assigned_object_id',
            ).contribute_to_class(VirtualDeviceContext, 'zabbix_hosts')

            GenericRelation(
                verbose_name=_('Zabbix Host Assignment'),
                to=ZabbixHost,
                related_name='virtual_chassis',
                related_query_name='virtual_chassis',
                content_type_field='assigned_object_type',
                object_id_field='assigned_object_id',
            ).contribute_to_class(VirtualChassis, 'zabbix_hosts')

            GenericRelation(
                verbose_name=_('Zabbix Host Assignment'),
                to=ZabbixHost,
                related_name='virtual_machines',
                related_query_name='virtual_machines',
                content_type_field='assigned_object_type',
                object_id_field='assigned_object_id',
            ).contribute_to_class(VirtualMachine, 'zabbix_hosts')
        except ImportError:
            pass


config = ZabbixPlugin
