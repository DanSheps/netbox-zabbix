import logging
import pprint

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django_rq import get_queue

from netbox import settings
from extras.models import Tag, TaggedItem
from dcim.models import Device
from netbox_zabbix.zabbix import Zabbix

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


def can_do_update(instance):
    if instance.get_config_context().get('zabbix', {}).get('groups', None) and \
            instance.device_type.custom_field_data.get('zabbix_group') == '':
        logger.debug(f'Zabbix({instance}): Appropriate groups not set')
        return False

    if not instance.primary_ip:
        logger.debug(f'Zabbix({instance}): Missing primary IP')
        return False

    if not instance.name:
        logger.debug(f'Zabbix({instance}): Missing name')
        return False

    tag_names = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('tags', None)
    logger.debug(f'{tag_names}')
    if tag_names is not None:
        if not isinstance(tag_names, list):
            tag_names = [tag_names]
        tag_ids = Tag.objects.filter(name__in=tag_names).values_list('id', flat=True)
        if instance.tags.filter(pk__in=[tag_ids]).count() == 0:
            logger.debug(f'Zabbix({instance.name}): Device does not match Zabbix automation tags')
            return False

    return True

def snmp_details(device):
    config_context = device.get_config_context()
    if config_context.get('zabbix', {}).get('snmp', None):
        snmp = None
        return config_context.get('zabbix', {}).get('snmp', {})
    else:
        return {}

def update_hostid(zabbix, device, name=None):
    host = zabbix.host_get(host=name)
    if host and host.get('hostid', None):
        device.skip_signal = True
        device.custom_field_data['zabbix_hostid'] = int(host.get('hostid'))
        device.save()
    else:
        logger.error(f'Zabbix({device.name}): Host ID not set and unable to locate host in Zabbix')
        return

def update_zabbix(pk, hostid=None):
    try:
        instance = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        logger.error(f'Zabbix({pk}): Device Instance not found')
        return

    status = 0
    if instance.status in ['offline', 'planned', 'inventory', 'staged']:
        status = 1

    if hasattr(instance, '_prechange_snapshot') and instance.name != instance._prechange_snapshot.get('name'):
        old_name = instance._prechange_snapshot.get('name')
    else:
        old_name = instance.name
    try:
        zabbix = Zabbix()
        snmp = snmp_details(device=instance)
        hostid = instance.custom_field_data.get('zabbix_hostid', None)

        if not hostid:
            update_hostid(zabbix, instance, old_name)
        elif hostid and not zabbix.host_get(hostid=hostid):
            update_hostid(zabbix, instance, old_name)
            instance.refresh_from_db()
            hostid = instance.custom_field_data.get('zabbix_hostid', None)

        template = zabbix.template_get(instance.device_type.get_full_name)
        if template is None:
            template = zabbix.template_get(f'{instance.device_type.manufacturer.name} {instance.device_type.part_number}')

        group = instance.get_config_context().get('zabbix', {}).get('groups', [])
        group.extend(instance.get_config_context().get('zabbix', {}).get('tenants', []))
        groups = []
        for gid in group:
            groups.append({'groupid': f"{gid}"})
        if len(groups) == 0:
            groups.append({'groupid': f"{settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('group', None)}"})
        if template:
            logger.info(f'Zabbix({instance.name}): Starting update')
            zabbix.host_update(
                hostid=instance.custom_field_data.get('zabbix_hostid', None),
                name=instance.name,
                ip=f'{instance.primary_ip.address.ip}',
                templates=[{'templateid': f"{template.get('templateid')}"}],
                groups=groups,
                snmp=snmp,
                status=status,
            )

            if not hostid:
                update_hostid(zabbix, instance, old_name)
            elif hostid and not zabbix.host_get(hostid=hostid):
                update_hostid(zabbix, instance, old_name)

            logger.info(f'Zabbix({instance.name}): Complete for {instance.name}')
        else:
            logger.error(f'Zabbix({instance.name}): No template set ("{instance.device_type.get_full_name}") ')
    except Exception as e:
        import traceback
        logger.error(f'Zabbix({instance.name}): Exception: {e}')
        logger.error(traceback.format_exc())


@receiver(post_save, sender=Device)
def update_device(instance, **kwargs):
    if hasattr(instance, 'skip_signal') and instance.skip_signal:
        return
    if can_do_update(instance):
        logger.debug('NetBox Zabbix: Hit Signal')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.signals.update_zabbix',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        logger.error(f'No update available for {instance}')

@receiver(m2m_changed, sender=TaggedItem)
def m2m_device(instance, **kwargs):
    if kwargs.get('action', None) not in ['post_add'] or not kwargs.get('pk_set') or not isinstance(instance, Device) \
            or hasattr(instance, 'skip_signal') and instance.skip_signal:
        return
    if can_do_update(instance):
        logger.debug('NetBox Zabbix: Hit M2M')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.signals.update_zabbix',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        logger.error(f'No update available for {instance}')
