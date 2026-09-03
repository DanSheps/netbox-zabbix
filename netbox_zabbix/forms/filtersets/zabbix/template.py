from django import forms
from django.utils.translation import gettext as _

from dcim.models import MACAddress
from netbox.forms import PrimaryModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from netbox_zabbix.models import *

__all__ = ('ZabbixTemplateFilterForm',)


class ZabbixTemplateFilterForm(PrimaryModelFilterSetForm):
    model = ZabbixTemplate
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet(
            'server_id',
        ),
        FieldSet('tag', name=_('Tags')),
    )

    server_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixServer.objects.all(),
        required=False,
        selector=True,
        label=_("Server"),
    )
    tag = TagFilterField(model)
