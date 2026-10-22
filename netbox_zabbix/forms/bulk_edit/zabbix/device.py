from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import PrimaryModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import BulkEditNullBooleanSelect

from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
    ZabbixHost,
)


__all__ = (
    'ZabbixDeviceBulkEditForm',
    'ZabbixVirtualMachineBulkEditForm',
)


class ZabbixDeviceBulkEditForm(PrimaryModelBulkEditForm):
    """Bulk edit form for ZabbixDevice."""
    zabbix_host = DynamicModelChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=False,
        label=_('Zabbix Host'),
    )
    sync_enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
        label=_('Sync Enabled'),
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label=_('Description'),
    )

    model = ZabbixDevice
    fieldsets = (
        FieldSet(
            'zabbix_host',
            'sync_enabled',
            'description',
        ),
    )
    nullable_fields = (
        'description',
        'comments',
        'tags',
    )


class ZabbixVirtualMachineBulkEditForm(PrimaryModelBulkEditForm):
    """Bulk edit form for ZabbixVirtualMachine."""
    zabbix_host = DynamicModelChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=False,
        label=_('Zabbix Host'),
    )
    sync_enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
        label=_('Sync Enabled'),
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label=_('Description'),
    )

    model = ZabbixVirtualMachine
    fieldsets = (
        FieldSet(
            'zabbix_host',
            'sync_enabled',
            'description',
        ),
    )
    nullable_fields = (
        'description',
        'comments',
        'tags',
    )

