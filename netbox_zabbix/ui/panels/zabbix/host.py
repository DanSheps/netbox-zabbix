# from django.contrib.contenttypes.models import ContentType
# from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from netbox.ui import actions, attrs, panels
from netbox_zabbix.ui.attrs.hyperlink import HyperLinkAttr
from netbox_zabbix.ui.panels.zabbix._base import ZabbixIDPanel

__all__ = (
    'ZabbixHostGroupPanel',
    'ZabbixHostPanel',
    'ZabbixHostInterfacePanel',
    'ZabbixHostSNMPInterfacePanel',
    'ZabbixManagedHostTemplatePanel',
)


class ZabbixHostGroupPanel(ZabbixIDPanel, panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class ZabbixHostPanel(ZabbixIDPanel, panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class ZabbixHostInterfacePanel(ZabbixIDPanel, panels.ObjectAttributesPanel):
    host = attrs.TextAttr('host')
    type = attrs.TextAttr('type')
    connection = attrs.TextAttr('connection')
    ip = attrs.TextAttr('ip')
    dns = attrs.TextAttr('dns')
    port = attrs.TextAttr('port')
    description = attrs.TextAttr('description')


class ZabbixHostSNMPInterfacePanel(panels.ObjectAttributesPanel):
    version = attrs.TextAttr('version')
    community = attrs.TextAttr('community')
    context_name = attrs.TextAttr('context_name')
    security_name = attrs.TextAttr('security')
    security_level = attrs.TextAttr('security_level')
    auth_protocol = attrs.TextAttr('auth_protocol')
    auth_passphrase = attrs.TextAttr('auth_passphrase')
    privacy_protocol = attrs.TextAttr('privacy_protocol')
    privacy_passphrase = attrs.TextAttr('privacy_passphrase')


class ZabbixManagedHostTemplatePanel(ZabbixIDPanel, panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    managed = attrs.BooleanAttr('managed')
    description = attrs.TextAttr('description')
