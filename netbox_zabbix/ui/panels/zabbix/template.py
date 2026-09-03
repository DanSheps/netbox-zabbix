# from django.contrib.contenttypes.models import ContentType
# from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from netbox.ui import actions, attrs, panels
from netbox_zabbix.ui.attrs.hyperlink import HyperLinkAttr


__all__ = ('ZabbixTemplatePanel',)


class ZabbixTemplatePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')