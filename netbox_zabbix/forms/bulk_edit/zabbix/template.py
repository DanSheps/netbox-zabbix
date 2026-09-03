from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import PrimaryModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import BulkEditNullBooleanSelect

from netbox_zabbix.models import ZabbixTemplate


__all__ = ('ZabbixTemplateBulkEditForm',)


class ZabbixTemplateBulkEditForm(PrimaryModelBulkEditForm):

    model = ZabbixTemplate
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description', 'comments')
