import logging

from dcim.models import Device
from virtualization.models import VirtualMachine

from netbox_zabbix.utilities.zabbix import update_zabbix

__all__ = (
    'update_zabbix_device',
    'update_zabbix_vm',
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
