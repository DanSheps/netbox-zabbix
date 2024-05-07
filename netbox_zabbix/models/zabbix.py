from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse

from netbox.models import NetBoxModel


__all__ = (
    'ZabbixHost',
)


class ZabbixHost(NetBoxModel):
    name = models.CharField(
        max_length=255
    )
    hostname = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ['name', ]
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Name must be unique."
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_zabbix:zabbixhost', args=[self.pk])
