from django import forms
from django.utils.translation import gettext as _

from netbox.forms import PrimaryModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
    ZabbixHost,
)
from dcim.models import Device
from virtualization.models import VirtualMachine


__all__ = (
    'ZabbixDeviceFilterForm',
    'ZabbixVirtualMachineFilterForm',
)


class ZabbixDeviceFilterForm(PrimaryModelFilterSetForm):
    """FilterSet form for ZabbixDevice."""
    model = ZabbixDevice

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    zabbix_host_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=False,
        selector=True,
        label=_('Zabbix Host'),
    )
    sync_enabled = forms.NullBooleanField(
        required=False,
        label=_('Sync Enabled'),
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
        ),
        FieldSet(
            'device_id',
            'zabbix_host_id',
            'sync_enabled',
        ),
        FieldSet('tag', name=_('Tags')),
    )


class ZabbixVirtualMachineFilterForm(PrimaryModelFilterSetForm):
    """FilterSet form for ZabbixVirtualMachine."""
    model = ZabbixVirtualMachine

    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machine'),
    )
    zabbix_host_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=False,
        selector=True,
        label=_('Zabbix Host'),
    )
    sync_enabled = forms.NullBooleanField(
        required=False,
        label=_('Sync Enabled'),
    )
    tag = TagFilterField(model)

    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
        ),
        FieldSet(
            'virtual_machine_id',
            'zabbix_host_id',
            'sync_enabled',
        ),
        FieldSet('tag', name=_('Tags')),
    )

