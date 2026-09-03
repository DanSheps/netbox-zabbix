import django_filters
from django.db.models import Q

from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from netbox_zabbix.choices import ZabbixHostInterfaceTypeChoices
from utilities.filtersets import register_filterset

from netbox_zabbix.models import *

__all__ = ('ZabbixTemplateFilterSet',)


@register_filterset
class ZabbixTemplateFilterSet(PrimaryModelFilterSet):
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
        label=_('Host Template (ID)'),
    )
    host_template = django_filters.ModelMultipleChoiceFilter(
        field_name="host_templates__name",
        queryset=ZabbixHostTemplate.objects.all(),
        to_field_name="name",
        label=_('Host Template (ID)'),
    )

    class Meta:
        model = ZabbixTemplate
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
