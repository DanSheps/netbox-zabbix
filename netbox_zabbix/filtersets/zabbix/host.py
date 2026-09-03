import django_filters
from django.db.models import Q

from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet, NetBoxModelFilterSet
from netbox_zabbix.choices import ZabbixHostInterfaceTypeChoices
from utilities.filtersets import register_filterset

from netbox_zabbix.models import *

__all__ = (
    'ZabbixHostGroupFilterSet',
    'ZabbixHostFilterSet',
    'ZabbixHostInterfaceFilterSet',
    'ZabbixHostInterfaceSNMPFilterSet',
)


@register_filterset
class ZabbixHostGroupFilterSet(PrimaryModelFilterSet):
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
    host_template_id = django_filters.ModelMultipleChoiceFilter(
        field_name='host_templates',
        queryset=ZabbixHostTemplate.objects.all(),
        label=_('Template (ID)'),
    )
    host_template = django_filters.ModelMultipleChoiceFilter(
        field_name="host_templates__name",
        queryset=ZabbixHostTemplate.objects.all(),
        to_field_name="name",
        label=_("Template (Name)"),
    )

    class Meta:
        model = ZabbixHostGroup
        fields = [
            'id',
            'q',
            'zid',
            'server_id',
            'server',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(name__icontains=value)

        return queryset.filter(qs_filter)


@register_filterset
class ZabbixHostFilterSet(PrimaryModelFilterSet):
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
        field_name='groups',
        queryset=ZabbixHostGroup.objects.all(),
        label=_('Host Group (ID)'),
    )
    group_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="groups__zid",
        queryset=ZabbixHostGroup.objects.all(),
        to_field_name="zid",
        label=_("Host Group (Zabbix ID)"),
    )
    group = django_filters.ModelMultipleChoiceFilter(
        field_name="groups__name",
        queryset=ZabbixHostGroup.objects.all(),
        to_field_name="name",
        label=_("Host Group (Name)"),
    )
    proxy_id = django_filters.ModelMultipleChoiceFilter(
        field_name='proxy',
        queryset=ZabbixProxy.objects.all(),
        label=_('Proxy (ID)'),
    )
    proxy_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="proxy__zid",
        queryset=ZabbixProxy.objects.all(),
        to_field_name="zid",
        label=_("Proxy (Zabbix ID)"),
    )
    proxy = django_filters.ModelMultipleChoiceFilter(
        field_name="proxy__name",
        queryset=ZabbixProxy.objects.all(),
        to_field_name="name",
        label=_("Proxy (Name)"),
    )
    proxy_group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='proxy_group',
        queryset=ZabbixProxyGroup.objects.all(),
        label=_('Proxy Group (ID)'),
    )
    proxy_group_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="proxy_group__zid",
        queryset=ZabbixProxyGroup.objects.all(),
        to_field_name="zid",
        label=_("Proxy Group (Zabbix ID)"),
    )
    proxy_group = django_filters.ModelMultipleChoiceFilter(
        field_name="proxy_group__name",
        queryset=ZabbixProxyGroup.objects.all(),
        to_field_name="name",
        label=_("Proxy Group (Name)"),
    )
    template_id = django_filters.ModelMultipleChoiceFilter(
        field_name='templates',
        queryset=ZabbixTemplate.objects.all(),
        label=_('Template (ID)'),
    )
    template_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="templates__zid",
        queryset=ZabbixTemplate.objects.all(),
        to_field_name="zid",
        label=_("Template (Zabbix ID)"),
    )
    template = django_filters.ModelMultipleChoiceFilter(
        field_name="templates__name",
        queryset=ZabbixTemplate.objects.all(),
        to_field_name="name",
        label=_("Template (Name)"),
    )

    class Meta:
        model = ZabbixHost
        fields = [
            'id',
            'q',
            'zid',
            'group_id',
            'group_zid',
            'group',
            'server_id',
            'server',
            'proxy_id',
            'proxy_zid',
            'proxy',
            'proxy_group_id',
            'proxy_group_zid',
            'proxy_group',
            'template_id',
            'template_zid',
            'template',
        ]


@register_filterset
class ZabbixHostInterfaceFilterSet(PrimaryModelFilterSet):
    host_id = django_filters.ModelMultipleChoiceFilter(
        field_name='host',
        queryset=ZabbixHost.objects.all(),
        label=_('Host (ID)'),
    )
    host_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="host__zid",
        queryset=ZabbixHost.objects.all(),
        to_field_name="name",
        label=_("Host (Zabbix ID)"),
    )

    class Meta:
        model = ZabbixHostInterface
        fields = [
            'id',
            'q',
            'zid',
            'type',
            'connection',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(ip__icontains=value)
        qs_filter |= Q(dns__icontains=value)

        return queryset.filter(qs_filter)


@register_filterset
class ZabbixHostInterfaceSNMPFilterSet(NetBoxModelFilterSet):
    interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name='interface',
        queryset=ZabbixHostInterface.objects.all(),
        label=_('Host Interface (ID)'),
    )
    interface_zid = django_filters.ModelMultipleChoiceFilter(
        field_name="interface__zid",
        queryset=ZabbixHostInterface.objects.all(),
        to_field_name="zid",
        label=_("Host Interface (Zabbix ID)"),
    )

    class Meta:
        model = ZabbixHostInterfaceSNMP
        fields = ['id', 'q']
