import django_tables2 as tables
from django.utils.translation import gettext_lazy as _


__all__ = ('ZabbixIDMixin', 'ZabbixMixin')


class ZabbixIDMixin:
    zid = tables.Column(
        linkify=True,
        verbose_name=_('Host'),
    )


class ZabbixMixin(ZabbixIDMixin):
    pass
