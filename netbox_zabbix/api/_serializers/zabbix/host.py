from rest_framework import serializers
from dcim.api.serializers_.devicetypes import DeviceTypeSerializer
from dcim.api.serializers_.platforms import PlatformSerializer
from dcim.api.serializers_.roles import DeviceRoleSerializer
from dcim.api.serializers_.sites import (
    RegionSerializer,
    SiteGroupSerializer,
    SiteSerializer,
    LocationSerializer,
)
from netbox.api.gfk_fields import GFKSerializerField
from netbox.api.serializers import PrimaryModelSerializer
from netbox_zabbix.api._serializers.zabbix.template import ZabbixTemplateSerializer

from netbox_zabbix.api._serializers.zabbix.server import (
    ZabbixProxyGroupSerializer,
    ZabbixProxySerializer,
)
from netbox_zabbix.models.zabbix.host import *


__all__ = (
    'ZabbixHostGroupSerializer',
    'ZabbixHostSerializer',
    'ZabbixHostInterfaceSerializer',
    'ZabbixHostInterfaceSNMPSerializer',
)

from tenancy.api.serializers_.tenants import TenantGroupSerializer, TenantSerializer

from virtualization.api.serializers_.clusters import (
    ClusterTypeSerializer,
    ClusterGroupSerializer,
    ClusterSerializer,
)


class ZabbixHostGroupSerializer(PrimaryModelSerializer):
    class Meta:
        model = ZabbixHostGroup
        fields = (
            'id',
            'url',
            'display',
            'name',
        )


class ZabbixHostSerializer(PrimaryModelSerializer):
    groups = ZabbixHostGroupSerializer(many=True, nested=True)
    proxy = ZabbixProxySerializer(nested=True)
    proxy_group = ZabbixProxyGroupSerializer(nested=True)
    assigned_object = GFKSerializerField(read_only=True)

    class Meta:
        model = ZabbixHost
        fields = (
            'id',
            'url',
            'display',
            'groups',
            'proxy',
            'proxy_group',
            'assigned_object_type',
            'assigned_object_id',
            'assigned_object',
        )


class ZabbixHostInterfaceSerializer(PrimaryModelSerializer):
    host = ZabbixHostSerializer(nested=True)

    class Meta:
        model = ZabbixHostInterface
        fields = (
            'id',
            'url',
            'display',
            'host',
            'type',
            'connection',
            'ip',
            'dns',
            'port',
        )


class ZabbixHostInterfaceSNMPSerializer(PrimaryModelSerializer):
    interface = ZabbixHostInterfaceSerializer(nested=True)

    class Meta:
        model = ZabbixHostInterfaceSNMP
        fields = (
            'id',
            'url',
            'display',
            'interface',
            'version',
            'community',
            'context_name',
            'security_name',
            'security_level',
            'auth_protocol',
            'auth_passphrase' 'priv_protocol',
            'priv_passphrase',
        )


class ZabbixManagedHostTemplate(PrimaryModelSerializer):
    name = serializers.CharField(max_length=255)
    managed = serializers.BooleanField(default=True)

    templates = ZabbixTemplateSerializer(many=True, nested=True)
    groups = ZabbixHostGroupSerializer(nested=True)

    regions = RegionSerializer(many=True, nested=True)
    site_groups = SiteGroupSerializer(many=True, nested=True)
    sites = SiteSerializer(many=True, nested=True)
    locations = LocationSerializer(many=True, nested=True)
    device_types = DeviceTypeSerializer(many=True, nested=True)
    roles = DeviceRoleSerializer(many=True, nested=True)
    platforms = PlatformSerializer(many=True, nested=True)
    cluster_types = ClusterTypeSerializer(many=True, nested=True)
    cluster_groups = ClusterGroupSerializer(many=True, nested=True)
    clusters = ClusterSerializer(many=True, nested=True)
    tenant_groups = TenantGroupSerializer(many=True, nested=True)
    tenants = TenantSerializer(many=True, nested=True)

    class Meta:
        model = ZabbixHostTemplate
        fields = (
            'id',
            'url',
            'display',
            'name',
            'auto_enroll',
            'templates',
            'groups',
            'regions',
            'site_groups',
            'sites',
            'locations',
            'device_types',
            'roles',
            'platforms',
            'cluster_types',
            'cluster_groups',
            'clusters',
            'tenant_groups',
            'tenants',
        )
