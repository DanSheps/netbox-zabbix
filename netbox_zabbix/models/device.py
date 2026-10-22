from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel


__all__ = (
    'ZabbixDevice',
    'ZabbixVirtualMachine',
)


class ZabbixDevice(NetBoxModel):
    """Tracks sync state between NetBox Device and Zabbix Host."""
    device = models.OneToOneField(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='zabbix_device'
    )
    zabbix_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Zabbix Host ID')
    )
    zabbix_host = models.OneToOneField(
        to='netbox_zabbix.ZabbixHost',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='device_sync'
    )
    sync_enabled = models.BooleanField(
        default=False,
        help_text=_('Enable bi-directional sync for this device')
    )
    last_synced = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Last sync timestamp')
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Description of device sync configuration')
    )

    class Meta:
        ordering = ('device', 'pk', )
        verbose_name = _('Zabbix Device Sync')
        verbose_name_plural = _('Zabbix Device Syncs')

    def __str__(self):
        return f'{self.device.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_zabbix:zabbixdevice', args=[self.pk])


class ZabbixVirtualMachine(NetBoxModel):
    """Tracks sync state between NetBox Virtual Machine and Zabbix Host."""
    virtual_machine = models.OneToOneField(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='zabbix_vm'
    )
    zabbix_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Zabbix Host ID')
    )
    zabbix_host = models.OneToOneField(
        to='netbox_zabbix.ZabbixHost',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vm_sync'
    )
    sync_enabled = models.BooleanField(
        default=False,
        help_text=_('Enable bi-directional sync for this virtual machine')
    )
    last_synced = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Last sync timestamp')
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Description of VM sync configuration')
    )

    class Meta:
        ordering = ('virtual_machine', 'pk', )
        verbose_name = _('Zabbix Virtual Machine Sync')
        verbose_name_plural = _('Zabbix Virtual Machine Syncs')

    def __str__(self):
        return f'{self.virtual_machine.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_zabbix:zabbixvirtualmachine', args=[self.pk])

