from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.urls import reverse

from choices import SNMPAuthChoices, SNMPPrivChoices
from netbox.models import NetBoxModel

from netbox_zabbix.choices import SNMPVersionChoices, SNMPSecurityChoices

__all__ = (
    'ZabbixSNMP',
)


class ZabbixSNMP(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    version = models.CharField(
        verbose_name=_('SNMP Version'),
        choices=SNMPVersionChoices,
    )
    community = models.CharField(
        verbose_name=_('Community String'),
        blank=True,
        null=True
    )
    context = models.CharField(
        verbose_name=_('Security Context'),
        blank=True,
        null=True
    )
    level = models.CharField(
        verbose_name=_('Security Level'),
        choices=SNMPSecurityChoices,
        blank=True,
        null=True
    )
    username = models.CharField(
        verbose_name=_('Usernanme'),
        blank=True,
        null=True
    )
    auth_protocol = models.CharField(
        verbose_name=_('Authentication Protocol'),
        choices=SNMPAuthChoices,
        blank=True,
        null=True
    )
    priv_protocol = models.CharField(
        verbose_name=_('Privacy Protocol'),
        choices=SNMPPrivChoices,
        blank=True,
        null=True
    )
    auth_passphrase = models.CharField(
        verbose_name=_('Authentication Passphrase'),
        blank=True,
        null=True
    )
    priv_passphrase = models.CharField(
        verbose_name=_('Privacy Passphrase'),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['assigned_object_type', 'assigned_object_id']
        constraints = ()

    def __str__(self):
        if self.assigned_object:
            return f'{self.assigned_object}'
        return '---Global---'

    def get_absolute_url(self):
        return reverse('plugins:netbox_zabbix:zabbixsnmp', args=[self.pk])\
