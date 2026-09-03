from django.db import models
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel, JobsMixin
from netbox_zabbix.models.zabbix.base import ZabbixID


__all__ = (
    'ZabbixServer',
    'ZabbixProxyGroup',
    'ZabbixProxy',
)


class ZabbixServer(JobsMixin, PrimaryModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    api_url = models.URLField(
        verbose_name=_('Base URL'),
    )
    api_token = models.CharField(
        max_length=255,
        verbose_name=_('Token'),
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Enable'),
    )
    validate_certificates = models.BooleanField(
        default=True,
        verbose_name=_('Validate SSL Certificates'),
        help_text=_(
            'Whether to validate SSL certificates when connecting to the Zabbix API.'
        ),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_name_unique',
            ),
            models.UniqueConstraint(
                fields=('api_url',),
                name='%(app_label)s_%(class)s_api_url_unique',
            ),
        ]

    def __str__(self):
        return self.name


class ZabbixProxyGroup(ZabbixID, PrimaryModel):
    server = models.ForeignKey(
        to=ZabbixServer,
        on_delete=models.CASCADE,
        related_name='proxy_groups',
        verbose_name=_('Server'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = 'Proxy Group'
        verbose_name_plural = 'Proxy Groups'
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

    @classmethod
    def get_zid_field_name(cls):
        return 'proxy_groupid'


class ZabbixProxy(ZabbixID, PrimaryModel):
    server = models.ForeignKey(
        to=ZabbixServer,
        on_delete=models.CASCADE,
        related_name='proxies',
        verbose_name=_('Server'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    group = models.ForeignKey(
        to=ZabbixProxyGroup,
        on_delete=models.CASCADE,
        related_name='proxies',
        verbose_name=_('Proxy Group'),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = 'Proxy'
        verbose_name_plural = 'Proxies'
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
