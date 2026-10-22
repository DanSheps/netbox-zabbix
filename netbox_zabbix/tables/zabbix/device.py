import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import PrimaryModelTable

from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
)
from netbox_zabbix.tables.zabbix._base import ZabbixMixin


__all__ = (
    'ZabbixDeviceTable',
    'ZabbixVirtualMachineTable',
)


class ZabbixDeviceTable(ZabbixMixin, PrimaryModelTable):
    """Table for displaying ZabbixDevice sync configurations."""
    device = tables.Column(
        linkify=True,
        verbose_name=_('Device'),
    )
    zabbix_host = tables.Column(
        linkify=True,
        verbose_name=_('Zabbix Host'),
    )
    sync_enabled = tables.BooleanColumn(
        verbose_name=_('Sync Enabled'),
    )
    last_synced = tables.DateTimeColumn(
        verbose_name=_('Last Synced'),
    )

    class Meta(PrimaryModelTable.Meta):
        model = ZabbixDevice
        fields = (
            'pk',
            'id',
            'device',
            'zabbix_host',
            'sync_enabled',
            'last_synced',
            'description',
        )
        default_columns = (
            'pk',
            'id',
            'device',
            'zabbix_host',
            'sync_enabled',
            'last_synced',
        )


class ZabbixVirtualMachineTable(ZabbixMixin, PrimaryModelTable):
    """Table for displaying ZabbixVirtualMachine sync configurations."""
    virtual_machine = tables.Column(
        linkify=True,
        verbose_name=_('Virtual Machine'),
    )
    zabbix_host = tables.Column(
        linkify=True,
        verbose_name=_('Zabbix Host'),
    )
    sync_enabled = tables.BooleanColumn(
        verbose_name=_('Sync Enabled'),
    )
    last_synced = tables.DateTimeColumn(
        verbose_name=_('Last Synced'),
    )

    class Meta(PrimaryModelTable.Meta):
        model = ZabbixVirtualMachine
        fields = (
            'pk',
            'id',
            'virtual_machine',
            'zabbix_host',
            'sync_enabled',
            'last_synced',
            'description',
        )
        default_columns = (
            'pk',
            'id',
            'virtual_machine',
            'zabbix_host',
            'sync_enabled',
            'last_synced',
        )

