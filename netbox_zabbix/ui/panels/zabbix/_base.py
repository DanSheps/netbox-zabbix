from django.utils.translation import gettext_lazy as _

from netbox.ui import actions, attrs, panels


__all__ = ('ZabbixIDPanel',)


class ZabbixIDPanel(panels.ObjectAttributesPanel):
    zid = attrs.TextAttr(
        'zid',
        label=_('Zabbix ID'),
    )
