import django_filters
from django.db.models import Q

from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from netbox_zabbix.choices import ZabbixHostInterfaceTypeChoices
from utilities.filtersets import register_filterset

from netbox_zabbix.models import *

__all__ = (
    'ZabbixServerFilterSet',
    'ZabbixProxyGroupFilterSet',
    'ZabbixProxyFilterSet',
)


@register_filterset
class ZabbixServerFilterSet(PrimaryModelFilterSet):

    class Meta:
        model = ZabbixServer
        fields = [
            'id',
            'q',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(name__icontains=value)

        return queryset.filter(qs_filter)


@register_filterset
class ZabbixProxyGroupFilterSet(PrimaryModelFilterSet):
    server_id = django_filters.ModelMultipleChoiceFilter(
        field_name='server',
        queryset=ZabbixServer.objects.all(),
        label=_('Server (ID)'),
    )
    server = django_filters.ModelMultipleChoiceFilter(
        field_name="server__name",
        queryset=ZabbixServer.objects.all(),
        to_field_name="name",
        label=_("Server (Name)"),
    )

    class Meta:
        model = ZabbixHost
        fields = [
            'id',
            'q',
            'zid',
            'server_id',
            'server',
        ]


@register_filterset
class ZabbixProxyFilterSet(PrimaryModelFilterSet):
    server_id = django_filters.ModelMultipleChoiceFilter(
        field_name='server',
        queryset=ZabbixServer.objects.all(),
        label=_('Server (ID)'),
    )
    server = django_filters.ModelMultipleChoiceFilter(
        field_name="server__name",
        queryset=ZabbixServer.objects.all(),
        to_field_name="name",
        label=_("Server (Name)"),
    )
    group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='group',
        queryset=ZabbixProxyGroup.objects.all(),
        label=_('Proxy Group (ID)'),
    )
    group_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="group__zid",
        queryset=ZabbixProxyGroup.objects.all(),
        to_field_name="zid",
        label=_("Proxy Group (Zabbix ID)"),
    )
    group = django_filters.ModelMultipleChoiceFilter(
        field_name="group__name",
        queryset=ZabbixProxyGroup.objects.all(),
        to_field_name="name",
        label=_("Proxy Group (Name)"),
    )

    class Meta:
        model = ZabbixProxy
        fields = [
            'id',
            'q',
            'zid',
            'group_id',
            'group_zid',
            'group',
            'server_id',
            'server',
        ]
