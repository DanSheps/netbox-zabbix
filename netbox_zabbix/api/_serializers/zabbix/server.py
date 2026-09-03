from netbox.api.serializers import PrimaryModelSerializer

from netbox_zabbix.models.zabbix.server import *


__all__ = (
    'ZabbixServerSerializer',
    'ZabbixProxyGroupSerializer',
    'ZabbixProxySerializer',
)


class ZabbixServerSerializer(PrimaryModelSerializer):
    class Meta:
        model = ZabbixServer
        fields = (
            'id',
            'url',
            'display',
            'name',
            'api_url',
            'api_token',
            'enabled',
            'validate_certificates',
        )


class ZabbixProxyGroupSerializer(PrimaryModelSerializer):
    class Meta:
        model = ZabbixProxyGroup
        fields = (
            'id',
            'url',
            'display',
            'name',
        )


class ZabbixProxySerializer(PrimaryModelSerializer):
    group = ZabbixProxyGroupSerializer(nested=True)

    class Meta:
        model = ZabbixProxy
        fields = (
            'id',
            'url',
            'display',
            'name',
            'group',
        )
