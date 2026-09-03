from netbox.api.viewsets import NetBoxModelViewSet

from netbox_zabbix.api.serializers import *
from netbox_zabbix.filtersets import *
from netbox_zabbix.models import *


__all__ = (
    'ZabbixServerViewSet',
    'ZabbixProxyGroupViewSet',
    'ZabbixProxyViewSet',
)


class ZabbixServerViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixServerFilterSet
    queryset = ZabbixServer.objects.all()
    serializer_class = ZabbixServerSerializer


class ZabbixProxyGroupViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixProxyGroupFilterSet
    queryset = ZabbixProxyGroup.objects.all()
    serializer_class = ZabbixProxyGroupSerializer


class ZabbixProxyViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixProxyFilterSet
    queryset = ZabbixProxy.objects.all()
    serializer_class = ZabbixProxySerializer
