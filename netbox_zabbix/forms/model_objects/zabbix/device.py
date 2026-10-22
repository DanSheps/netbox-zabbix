from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from netbox.forms import PrimaryModelForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
)
from utilities.forms.rendering import FieldSet

from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
    ZabbixHost,
)
from virtualization.models import VirtualMachine


__all__ = (
    'ZabbixDeviceForm',
    'ZabbixVirtualMachineForm',
)


class ZabbixDeviceForm(PrimaryModelForm):
    """Form for managing Device to Zabbix sync configuration."""
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        selector=True,
        label=_('Device'),
    )
    zabbix_host = DynamicModelChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=False,
        selector=True,
        label=_('Zabbix Host'),
        help_text=_('Associated Zabbix Host for this device'),
    )
    sync_enabled = forms.BooleanField(
        required=False,
        label=_('Enable Sync'),
        help_text=_('Enable bi-directional synchronization'),
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label=_('Description'),
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'device',
            'zabbix_host',
            'sync_enabled',
            name=_('Device Sync Configuration'),
        ),
        FieldSet(
            'description',
            name=_('Details'),
        ),
    )

    class Meta:
        model = ZabbixDevice
        fields = (
            'device',
            'zabbix_host',
            'zabbix_id',
            'sync_enabled',
            'description',
            'comments',
            'owner',
            'tags',
        )


class ZabbixVirtualMachineForm(PrimaryModelForm):
    """Form for managing Virtual Machine to Zabbix sync configuration."""
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=True,
        selector=True,
        label=_('Virtual Machine'),
    )
    zabbix_host = DynamicModelChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=False,
        selector=True,
        label=_('Zabbix Host'),
        help_text=_('Associated Zabbix Host for this virtual machine'),
    )
    sync_enabled = forms.BooleanField(
        required=False,
        label=_('Enable Sync'),
        help_text=_('Enable bi-directional synchronization'),
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label=_('Description'),
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'virtual_machine',
            'zabbix_host',
            'sync_enabled',
            name=_('Virtual Machine Sync Configuration'),
        ),
        FieldSet(
            'description',
            name=_('Details'),
        ),
    )

    class Meta:
        model = ZabbixVirtualMachine
        fields = (
            'virtual_machine',
            'zabbix_host',
            'zabbix_id',
            'sync_enabled',
            'description',
            'comments',
            'owner',
            'tags',
        )

