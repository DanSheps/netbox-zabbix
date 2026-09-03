from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import PrimaryModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import BulkEditNullBooleanSelect

from netbox_zabbix.models import ZabbixHostGroup, ZabbixHost, ZabbixHostInterface

__all__ = ('ZabbixHostGroupBulkEditForm', 'ZabbixHostBulkEditForm', 'ZabbixHostInterfaceBulkEditForm',)


class ZabbixHostGroupBulkEditForm(PrimaryModelBulkEditForm):
    # TODO: add server

    model = ZabbixHostGroup
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description', 'comments', 'tags',)


class ZabbixHostBulkEditForm(PrimaryModelBulkEditForm):
    # TODO: add server
    # TODO: add proxy
    # TODO: add groups

    model = ZabbixHost
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description', 'comments', 'tags', )


class ZabbixHostInterfaceBulkEditForm(PrimaryModelBulkEditForm):

    model = ZabbixHostInterface
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description', 'comments', 'tags', )
