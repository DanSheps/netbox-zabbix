import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, PrimaryModelTable

from netbox_zabbix.models import (
    ZabbixHostGroup,
    ZabbixHost,
    ZabbixHostInterface,
    ZabbixHostTemplate,
)
from netbox_zabbix.tables.zabbix._base import ZabbixMixin

__all__ = (
    'ZabbixHostGroupTable',
    'ZabbixHostTable',
    'ZabbixHostInterfaceTable',
    'ZabbixManagedHostTemplateTable',
)


class ZabbixHostGroupTable(ZabbixMixin, PrimaryModelTable):
    server = tables.Column(
        linkify=True,
        verbose_name=_('Server'),
    )

    class Meta(NetBoxTable.Meta):
        model = ZabbixHostGroup
        fields = (
            'pk',
            'id',
            'zid',
            'server',
            'name',
        )
        default_columns = (
            'pk',
            'id',
            'name',
        )


class ZabbixHostTable(ZabbixMixin, PrimaryModelTable):
    name = tables.Column(
        orderable=False,
        verbose_name=_('Name'),
        linkify=True,
    )
    server = tables.Column(
        linkify=True,
        verbose_name=_('Server'),
    )
    groups = tables.ManyToManyColumn(
        linkify_item=True,
        verbose_name=_('Groups'),
    )
    assigned_object_type = tables.Column(
        verbose_name=_('Assigned object type'),
        linkify=True,
    )
    assigned_object_id = tables.Column(
        verbose_name=_('Assigned object id'),
        linkify=True,
    )
    assigned_object = tables.Column(
        orderable=False,
        verbose_name=_('Assigned object'),
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = ZabbixHost
        fields = (
            'pk',
            'id',
            'zid',
            'name',
            'server',
            'assigned_object_type',
            'assigned_object_id',
            'assigned_object',
            'groups',
        )
        default_columns = (
            'pk',
            'id',
            'name',
            'assigned_object',
        )


class ZabbixHostInterfaceTable(ZabbixMixin, PrimaryModelTable):
    host = tables.Column(
        linkify=True,
        verbose_name=_('Host'),
    )
    type = tables.Column(
        orderable=True,
        verbose_name=_('Type'),
    )
    connection = tables.Column(
        orderable=True,
        verbose_name=_('Connection'),
    )
    ip = tables.Column(
        orderable=True,
        verbose_name=_('IP Address'),
    )
    dns = tables.Column(
        orderable=True,
        verbose_name=_('DNS'),
    )
    port = tables.Column(
        orderable=True,
        verbose_name=_('Port'),
    )

    class Meta(NetBoxTable.Meta):
        model = ZabbixHostInterface
        fields = ('pk', 'id', 'zid', 'host', 'type', 'connection', 'ip', 'dns', 'port')
        default_columns = (
            'pk',
            'id',
            'host',
            'type',
        )


class ZabbixManagedHostTemplateTable(ZabbixMixin, PrimaryModelTable):

    class Meta(NetBoxTable.Meta):
        model = ZabbixHostTemplate
        fields = (
            'pk',
            'id',
            'name',
            'managed',
            'description',
            'groups',
            'templates',
            'regions',
            'site_groups',
            'sites',
            'locations',
            'device_type',
            'roles',
            'platforms',
            'cluster_types',
            'cluster_groups',
            'clusters',
            'tenant_groups',
            'tenants',
            'owner',
            'tags',
        )
        default_columns = (
            'pk',
            'id',
            'name',
        )
