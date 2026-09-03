from django import forms
from django.utils.translation import gettext as _

from dcim.models import MACAddress
from netbox.forms import PrimaryModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from netbox_zabbix.models import *

__all__ = (
    'ZabbixHostGroupFilterForm',
    'ZabbixHostFilterForm',
)


class ZabbixHostGroupFilterForm(PrimaryModelFilterSetForm):
    model = ZabbixHostGroup
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


class ZabbixHostFilterForm(PrimaryModelFilterSetForm):
    model = ZabbixHost
    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
        ),
        FieldSet(
            'template_id',
            'server_id',
            'group_id',
            'proxy_group_id',
            'proxy_id',
        ),
        FieldSet('tag', name=_('Tags')),
    )

    server_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixServer.objects.all(),
        required=False,
        selector=True,
        label=_("Servers"),
    )
    proxy_group_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixProxyGroup.objects.all(),
        required=False,
        selector=True,
        label=_("Zabbix Proxy Groups"),
    )
    proxy_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixProxy.objects.all(),
        required=False,
        selector=True,
        label=_("Proxies"),
    )
    template_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixTemplate.objects.all(),
        required=False,
        selector=True,
        label=_("Templates"),
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=ZabbixHostGroup.objects.all(),
        required=False,
        selector=True,
        label=_("Host Groups"),
    )
    tag = TagFilterField(model)
