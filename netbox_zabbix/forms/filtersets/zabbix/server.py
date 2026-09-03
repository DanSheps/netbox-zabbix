from django import forms
from django.utils.translation import gettext as _

from dcim.models import MACAddress
from netbox.forms import PrimaryModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from netbox_zabbix.models import ZabbixServer, ZabbixProxy, ZabbixProxyGroup

__all__ = ('ZabbixServerFilterForm',)


class ZabbixServerFilterForm(PrimaryModelFilterSetForm):
    model = ZabbixServer
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('tag', name=_('Tags')),
    )


class ZabbixProxyFilterForm(PrimaryModelFilterSetForm):
    model = ZabbixProxy
    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
        ),
        FieldSet(
            'server_id',
            'group_id',
        ),
        FieldSet('tags', name=_('Tags')),
    )

    server_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixServer.objects.all(),
        required=False,
        selector=True,
        label=_("Server"),
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixProxyGroup.objects.all(),
        required=False,
        selector=True,
        label=_("Proxy Group"),
    )
    tag = TagFilterField(model)


class ZabbixProxyFilterForm(PrimaryModelFilterSetForm):
    model = ZabbixProxyGroup
    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
        ),
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
