from netbox.api.serializers import PrimaryModelSerializer
from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
    ZabbixHost,
)


__all__ = (
    'ZabbixDeviceSerializer',
    'ZabbixVirtualMachineSerializer',
)


class ZabbixDeviceSerializer(PrimaryModelSerializer):
    """Serializer for ZabbixDevice model."""
    class Meta:
        model = ZabbixDevice
        fields = (
            'id',
            'url',
            'display',
            'device',
            'zabbix_id',
            'zabbix_host',
            'sync_enabled',
            'last_synced',
            'description',
            'comments',
            'owner',
            'tags',
            'created',
            'last_updated',
        )


class ZabbixVirtualMachineSerializer(PrimaryModelSerializer):
    """Serializer for ZabbixVirtualMachine model."""
    class Meta:
        model = ZabbixVirtualMachine
        fields = (
            'id',
            'url',
            'display',
            'virtual_machine',
            'zabbix_id',
            'zabbix_host',
            'sync_enabled',
            'last_synced',
            'description',
            'comments',
            'owner',
            'tags',
            'created',
            'last_updated',
        )

