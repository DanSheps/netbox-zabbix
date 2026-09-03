import logging

from core.choices import ObjectChangeActionChoices
from dcim.models import Device, VirtualDeviceContext
from extras.models import Tag
from netbox import settings
from virtualization.models import VirtualMachine


__all__ = (
    'can_do_update',
    'snmp_details',
    'has_changes',
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')


def has_changes(instance, action=ObjectChangeActionChoices.ACTION_UPDATE):
    if not hasattr(instance, "pk") or not instance.pk:
        return True
    return instance.to_objectchange(action).has_changes


def can_do_update(instance):
    instance.refresh_from_db()
    if isinstance(instance, Device):
        if (
            not instance.get_config_context().get('zabbix', {}).get('groups', None)
            and instance.device_type.custom_field_data.get('zabbix_group') == ''
        ):
            logger.debug(f'Zabbix({instance}): Appropriate Device groups not set')
            return False
    elif isinstance(instance, VirtualDeviceContext):
        if (
            not instance.device.get_config_context()
            .get('zabbix', {})
            .get('groups', None)
            and instance.device.device_type.custom_field_data.get('zabbix_group') == ''
        ):
            logger.debug(f'Zabbix({instance}): Appropriate Device groups not set')
            return False
    elif isinstance(instance, VirtualMachine):
        if not instance.get_config_context().get('zabbix', {}).get('groups', None):
            logger.debug(f'Zabbix({instance}): Appropriate VM groups not set')
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
            logger.debug(f'{tag_names}:{tag_ids}')
            logger.debug(f'{instance.tags.all()}')
            logger.debug(f'{instance.tags.filter(pk__in=[tag_ids]).count()}')
            logger.debug(
                f'Zabbix({instance.name}): Device does not match Zabbix automation tags'
            )
            return False

    return True


def snmp_details(instance):
    device = instance
    if isinstance(instance, VirtualDeviceContext):
        device = instance.device
    config_context = device.get_config_context()
    if config_context.get('zabbix', {}).get('snmp', None):
        snmp = None
        return config_context.get('zabbix', {}).get('snmp', {})
    else:
        return {}
