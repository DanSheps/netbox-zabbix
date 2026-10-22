from .host import *
from .server import *
from .template import *
from .device import *

__all__ = (
    'ZabbixHostGroupViewSet',
    'ZabbixHostInterfaceViewSet',
    'ZabbixHostInterfaceSNMPViewSet',
    'ZabbixHostViewSet',
    'ZabbixProxyGroupViewSet',
    'ZabbixProxyViewSet',
    'ZabbixServerViewSet',
    'ZabbixTemplateViewSet',
    'ZabbixDeviceViewSet',
    'ZabbixVirtualMachineViewSet',
)
