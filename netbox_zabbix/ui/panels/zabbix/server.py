# from django.contrib.contenttypes.models import ContentType
# from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from netbox.ui import actions, attrs, panels
from netbox_zabbix.ui.attrs.hyperlink import HyperLinkAttr


__all__ = (
    'ZabbixServerPanel',
    'ZabbixProxyGroupPanel',
    'ZabbixProxyPanel',
)


class ZabbixServerPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    api_url = HyperLinkAttr(
        'api_url',
        copy_button=True,
        label=_('API URL'),
    )
    api_token = attrs.TextAttr(
        'api_token',
        label=_('API Token'),
    )
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True, grouped_by='group')
    description = attrs.TextAttr('description')


class ZabbixProxyGroupPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    server = attrs.RelatedObjectAttr('server', linkify=True)
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True, grouped_by='group')
    description = attrs.TextAttr('description')


class ZabbixProxyPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    server = attrs.RelatedObjectAttr('server', linkify=True)
    group = attrs.RelatedObjectAttr('group', linkify=True)
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True, grouped_by='group')
    description = attrs.TextAttr('description')
