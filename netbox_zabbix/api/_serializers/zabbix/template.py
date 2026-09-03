from netbox.api.serializers import PrimaryModelSerializer

from netbox_zabbix.models.zabbix.template import *


__all__ = ('ZabbixTemplateSerializer',)


class ZabbixTemplateSerializer(PrimaryModelSerializer):
    class Meta:
        model = ZabbixTemplate
        fields = (
            'id',
            'url',
            'display',
            'name',
        )
