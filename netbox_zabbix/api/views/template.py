from netbox.api.viewsets import NetBoxModelViewSet

from netbox_zabbix.api.serializers import *
from netbox_zabbix.filtersets import *
from netbox_zabbix.models import *


__all__ = ('ZabbixTemplateViewSet',)


class ZabbixTemplateViewSet(NetBoxModelViewSet):
    filterset_class = ZabbixTemplateFilterSet
    queryset = ZabbixTemplate.objects.all()
    serializer_class = ZabbixTemplateSerializer
