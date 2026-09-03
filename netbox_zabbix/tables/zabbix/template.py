import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, PrimaryModelTable

from netbox_zabbix.models import ZabbixTemplate
from netbox_zabbix.tables.zabbix._base import ZabbixMixin

__all__ = ('ZabbixTemplateTable',)


class ZabbixTemplateTable(ZabbixMixin, PrimaryModelTable):
    server = tables.Column(
        linkify=True,
        verbose_name=_('Server'),
    )

    class Meta(NetBoxTable.Meta):
        model = ZabbixTemplate
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
