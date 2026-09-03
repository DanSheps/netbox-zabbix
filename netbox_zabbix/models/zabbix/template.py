from django.db import models
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel
from netbox_zabbix.models.zabbix.base import ZabbixID


class ZabbixTemplate(ZabbixID, PrimaryModel):
    server = models.ForeignKey(
        to='netbox_zabbix.ZabbixServer',
        on_delete=models.CASCADE,
        related_name='templates',
        verbose_name=_('Zabbix Server'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    class Meta:
        ordering = (
            'server',
            'name',
        )
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'server',
                    'zid',
                ),
                name='%(app_label)s_%(class)s_server_zid_unique',
            ),
            models.UniqueConstraint(
                fields=(
                    'server',
                    'name',
                ),
                name='%(app_label)s_%(class)s_server_name_unique',
            ),
        ]

    def __str__(self):
        return self.name
