from .server import *
from .host import *
from .template import *
from .device import *

__all__ = (
    'ZabbixServerTable',
    'ZabbixHostTable',
    'ZabbixTemplateTable',
    'ZabbixHostGroupTable',
    'ZabbixHostInterfaceTable',
    'ZabbixManagedHostTemplateTable',
    'ZabbixProxyTable',
    'ZabbixProxyGroupTable',
    'ZabbixDeviceTable',
    'ZabbixVirtualMachineTable',
)
