import logging

from dcim.models import Device
from extras.models import Tag
from netbox import settings
from virtualization.models import VirtualMachine


__all__ = (
    'can_do_update',
    'snmp_details',
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')


def can_do_update(instance):
    if (
        (
            isinstance(instance, Device) and not instance.get_config_context().get('zabbix', {}).get('groups', None) and
            instance.device_type.custom_field_data.get('zabbix_group') == ''
        ) or (
            isinstance(instance, VirtualMachine) and
            not instance.get_config_context().get('zabbix', {}).get('groups', None)
        )
    ):
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
