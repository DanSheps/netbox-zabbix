from netbox.api.viewsets import NetBoxModelViewSet

from netbox_zabbix.api.serializers import *
from netbox_zabbix.filtersets import *
from netbox_zabbix.models import *


__all__ = (
    'ZabbixHostGroupViewSet',
    'ZabbixHostViewSet',
    'ZabbixHostInterfaceViewSet',
    'ZabbixHostInterfaceSNMPViewSet',
)


class ZabbixHostGroupViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixHostGroupFilterSet
    queryset = ZabbixHostGroup.objects.all()
    serializer_class = ZabbixHostGroupSerializer


class ZabbixHostViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixHostFilterSet
    queryset = ZabbixHost.objects.all()
    serializer_class = ZabbixHostSerializer


class ZabbixHostInterfaceViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixHostInterfaceFilterSet
    queryset = ZabbixHostInterface.objects.all()
    serializer_class = ZabbixHostInterfaceSerializer


class ZabbixHostInterfaceSNMPViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixHostInterfaceSNMPFilterSet
    queryset = ZabbixHostInterfaceSNMP.objects.all()
    serializer_class = ZabbixHostInterfaceSNMPSerializer
