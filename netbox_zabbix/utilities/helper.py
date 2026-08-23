import logging
import re

from dcim.models import Device
from extras.models import Tag
from netbox import settings
from virtualization.models import VirtualMachine


__all__ = (
    'can_do_update',
    'snmp_details',
    'slugify_name',
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')


# Транслитерация кириллицы → латиница (Zabbix не принимает не-ASCII в именах хостов)
_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
    'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
    'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
}


def slugify_name(name):
    """Транслитерировать кириллицу и привести к формату, допустимому в Zabbix (A-Za-z0-9._-)."""
    if not name:
        return name
    out = ''.join(_TRANSLIT.get(c, c) for c in name)
    out = re.sub(r'[^A-Za-z0-9._\-]', '-', out)
    return out


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
