import logging

from dcim.models import Device
from virtualization.models import VirtualMachine

from netbox_zabbix.zabbix import Zabbix
from netbox_zabbix.utilities.helper import slugify_name
from netbox_zabbix.utilities.zabbix import update_zabbix

__all__ = (
    'update_zabbix_device',
    'update_zabbix_vm',
    'delete_zabbix_device',
    'delete_zabbix_vm',
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')


def update_zabbix_device(pk, hostid=None):
    try:
        instance = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        logger.error(f'Zabbix({pk}): Device Instance not found')
        return

    update_zabbix(instance=instance, hostid=hostid)


def update_zabbix_vm(pk, hostid=None):
    try:
        instance = VirtualMachine.objects.get(pk=pk)
    except Device.DoesNotExist:
        logger.error(f'Zabbix({pk}): Device Instance not found')
        return

    update_zabbix(instance=instance, hostid=hostid)


def delete_zabbix_device(hostid=None, name=None):
    try:
        zabbix = Zabbix()
        # Host name in Zabbix is transliterated, not the original (Cyrillic is not allowed)
        result = zabbix.host_delete(hostid=hostid, name=slugify_name(name) if name else None)
        logger.info(f'Zabbix delete ({name}): {result}')
    except Exception as e:
        logger.error(f'Zabbix delete ({name}): Exception: {e}')


def delete_zabbix_vm(hostid=None, name=None):
    delete_zabbix_device(hostid=hostid, name=name)
