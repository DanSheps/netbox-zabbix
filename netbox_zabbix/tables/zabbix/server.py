import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, PrimaryModelTable

from netbox_zabbix.models import ZabbixServer, ZabbixProxy, ZabbixProxyGroup
from netbox_zabbix.tables.zabbix._base import ZabbixMixin

__all__ = (
    'ZabbixServerTable',
    'ZabbixProxyTable',
    'ZabbixProxyGroupTable',
)


class ZabbixServerTable(PrimaryModelTable):
    api_url = tables.URLColumn(verbose_name=_('API URL'))

    class Meta(NetBoxTable.Meta):
        model = ZabbixServer
        fields = (
            'pk',
            'id',
            'name',
            'api_url',
            'api_token',
            'enabled',
            'validate_certificates',
        )
        default_columns = (
            'pk',
            'id',
            'name',
            'api_url',
        )


class ZabbixProxyTable(ZabbixMixin, PrimaryModelTable):
    server = tables.Column(
        linkify=True,
        verbose_name=_('Server'),
    )
    group = tables.Column(
        linkify=True,
        verbose_name=_('Group'),
    )

    class Meta(NetBoxTable.Meta):
        model = ZabbixProxy
        fields = ('pk', 'id', 'zid', 'server', 'name', 'group')
        default_columns = (
            'pk',
            'id',
            'name',
        )


class ZabbixProxyGroupTable(ZabbixMixin, PrimaryModelTable):
    server = tables.Column(
        linkify=True,
        verbose_name=_('Server'),
    )

    class Meta(NetBoxTable.Meta):
        model = ZabbixProxyGroup
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
