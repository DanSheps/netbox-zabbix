from netbox.api.viewsets import NetBoxModelViewSet

from netbox_zabbix.api.serializers import (
    ZabbixDeviceSerializer,
    ZabbixVirtualMachineSerializer,
)
from netbox_zabbix.filtersets import (
    ZabbixDeviceFilterSet,
    ZabbixVirtualMachineFilterSet,
)
from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
)


__all__ = (
    'ZabbixDeviceViewSet',
    'ZabbixVirtualMachineViewSet',
)


class ZabbixDeviceViewSet(NetBoxModelViewSet):
    """ViewSet for ZabbixDevice model."""
    filterset_class = ZabbixDeviceFilterSet
    queryset = ZabbixDevice.objects.all()
    serializer_class = ZabbixDeviceSerializer


class ZabbixVirtualMachineViewSet(NetBoxModelViewSet):
    """ViewSet for ZabbixVirtualMachine model."""
    filterset_class = ZabbixVirtualMachineFilterSet
    queryset = ZabbixVirtualMachine.objects.all()
    serializer_class = ZabbixVirtualMachineSerializer

