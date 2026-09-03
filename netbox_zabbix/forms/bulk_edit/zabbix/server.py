from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import PrimaryModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import BulkEditNullBooleanSelect

from netbox_zabbix.models import ZabbixServer, ZabbixProxy, ZabbixProxyGroup

__all__ = ('ZabbixServerBulkEditForm', 'ZabbixProxyGroupBulkEditForm', 'ZabbixProxyBulkEditForm')


class ZabbixServerBulkEditForm(PrimaryModelBulkEditForm):
    enabled = forms.BooleanField(required=False, label=_('Enabled'))

    model = ZabbixServer
    fieldsets = (
        FieldSet(
            'enabled',
            'description',
        ),
    )
    nullable_fields = ('description', 'comments')


class ZabbixProxyGroupBulkEditForm(PrimaryModelBulkEditForm):

    model = ZabbixProxyGroup
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description', 'comments', 'tags')


class ZabbixProxyBulkEditForm(PrimaryModelBulkEditForm):

    model = ZabbixProxy
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description', 'comments', 'tags')
