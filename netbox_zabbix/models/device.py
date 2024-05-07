from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel


__all__ = (
    'ZabbixDevice',
)


class ZabbixDevice(NetBoxModel):
    device = models.OneToOneField(
        to='dcim.Device',
        on_delete=models.CASCADE
    )
    zabbix_id = models.IntegerField()
    sync = models.BooleanField()

    class Meta:
        ordering = ['device']
        constraints = ()

    def __str__(self):
        return f'{self.device.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_zabbix:zabbixdevice', args=[self.pk])\
