import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Device
from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from virtualization.models import VirtualMachine

from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
    ZabbixHost,
)


__all__ = (
    'ZabbixDeviceFilterSet',
    'ZabbixVirtualMachineFilterSet',
)


@register_filterset
class ZabbixDeviceFilterSet(PrimaryModelFilterSet):
    """FilterSet for ZabbixDevice objects."""
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label=_('Device (ID)'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label=_('Device (Name)'),
    )
    zabbix_host_id = django_filters.ModelMultipleChoiceFilter(
        field_name='zabbix_host',
        queryset=ZabbixHost.objects.all(),
        label=_('Zabbix Host (ID)'),
    )
    zabbix_host = django_filters.ModelMultipleChoiceFilter(
        field_name='zabbix_host__name',
        queryset=ZabbixHost.objects.all(),
        to_field_name='name',
        label=_('Zabbix Host (Name)'),
    )
    sync_enabled = django_filters.BooleanFilter(
        field_name='sync_enabled',
        label=_('Sync Enabled'),
    )

    class Meta:
        model = ZabbixDevice
        fields = [
            'id',
            'q',
            'sync_enabled',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(device__name__icontains=value)
        qs_filter |= Q(description__icontains=value)

        return queryset.filter(qs_filter)


@register_filterset
class ZabbixVirtualMachineFilterSet(PrimaryModelFilterSet):
    """FilterSet for ZabbixVirtualMachine objects."""
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine',
        queryset=VirtualMachine.objects.all(),
        label=_('Virtual Machine (ID)'),
    )
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine__name',
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        label=_('Virtual Machine (Name)'),
    )
    zabbix_host_id = django_filters.ModelMultipleChoiceFilter(
        field_name='zabbix_host',
        queryset=ZabbixHost.objects.all(),
        label=_('Zabbix Host (ID)'),
    )
    zabbix_host = django_filters.ModelMultipleChoiceFilter(
        field_name='zabbix_host__name',
        queryset=ZabbixHost.objects.all(),
        to_field_name='name',
        label=_('Zabbix Host (Name)'),
    )
    sync_enabled = django_filters.BooleanFilter(
        field_name='sync_enabled',
        label=_('Sync Enabled'),
    )

    class Meta:
        model = ZabbixVirtualMachine
        fields = [
            'id',
            'q',
            'sync_enabled',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(virtual_machine__name__icontains=value)
        qs_filter |= Q(description__icontains=value)

        return queryset.filter(qs_filter)




