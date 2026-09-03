from django.utils.translation import gettext as _

from netbox.forms import PrimaryModelForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
)

from netbox_zabbix.models import ZabbixServer, ZabbixProxy, ZabbixProxyGroup

__all__ = ('ZabbixServerForm', 'ZabbixProxyGroupForm', 'ZabbixProxyForm')

from utilities.forms.rendering import FieldSet


class ZabbixServerForm(PrimaryModelForm):

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'name',
            'enabled',
        ),
        FieldSet('api_url', 'api_token', 'validate_certificates', name=_('API')),
    )

    class Meta:
        model = ZabbixServer
        fields = (
            'name',
            'enabled',
            'api_url',
            'api_token',
            'validate_certificates',
            'description',
            'comments',
            'owner',
            'tags',
        )


class ZabbixProxyGroupForm(PrimaryModelForm):
    server = DynamicModelChoiceField(
        queryset=ZabbixServer.objects.all(),
        required=True,
        selector=True,
        label=_('Zabbix Server'),
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'server',
            'name',
        ),
    )

    class Meta:
        model = ZabbixProxyGroup
        fields = (
            'server',
            'name',
            'description',
            'comments',
            'owner',
            'tags',
        )


class ZabbixProxyForm(PrimaryModelForm):
    server = DynamicModelChoiceField(
        queryset=ZabbixServer.objects.all(),
        required=True,
        selector=True,
        label=_('Zabbix Server'),
    )
    group = DynamicModelChoiceField(
        queryset=ZabbixProxyGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Proxy Group'),
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'server',
            'name',
            'group',
        ),
    )

    class Meta:
        model = ZabbixProxy
        fields = (
            'server',
            'name',
            'group',
            'description',
            'comments',
            'owner',
            'tags',
        )
