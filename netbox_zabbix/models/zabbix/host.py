from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from ipam.models import IPAddress
from netbox.models import PrimaryModel, NetBoxModel, JobsMixin

from netbox_zabbix.choices import (
    ZabbixHostInterfaceTypeChoices,
    ZabbixHostInterfaceConnectionChoices,
)
from netbox_zabbix.choices.zabbix import (
    ZabbixHostInterfaceSNMPVersionChoices,
    ZabbixHostInterfaceSNMPAuthProtocolChoices,
    ZabbixHostInterfaceSNMPSecurityChoices,
    ZabbixHostInterfaceSNMPPrivacyProtocolChoices,
)
from netbox_zabbix.constants import ZABBIX_ASSIGNMENT_MODELS
from netbox_zabbix.models.zabbix.base import ZabbixID
from netbox_zabbix.models.zabbix.server import (
    ZabbixServer,
    ZabbixProxy,
    ZabbixProxyGroup,
)


class ZabbixHostGroup(ZabbixID, PrimaryModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    server = models.ForeignKey(
        to=ZabbixServer,
        on_delete=models.CASCADE,
        related_name='host_groups',
        verbose_name=_('Zabbix Server'),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Host Group'
        verbose_name_plural = 'Host Groups'
        constraints = [
            models.UniqueConstraint(
                fields=('zid',),
                name='%(app_label)s_%(class)s_server_zid_unique',
            ),
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_server_name_unique',
            ),
        ]

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_zid_field_name(cls):
        return 'groupid'


class ZabbixHost(JobsMixin, ZabbixID, PrimaryModel):
    server = models.ForeignKey(
        to=ZabbixServer,
        on_delete=models.CASCADE,
        related_name='hosts',
        verbose_name=_('Zabbix Server'),
    )
    proxy = models.ForeignKey(
        to=ZabbixProxy,
        on_delete=models.CASCADE,
        related_name='hosts',
        verbose_name=_('Zabbix Proxy'),
        blank=True,
        null=True,
    )
    proxy_group = models.ForeignKey(
        to=ZabbixProxyGroup,
        on_delete=models.CASCADE,
        related_name='hosts',
        verbose_name=_('Zabbix Proxy Group'),
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        to='ZabbixHostGroup',
        related_name='hosts',
        verbose_name=_('Host Groups'),
    )
    templates = models.ManyToManyField(
        to='netbox_zabbix.ZabbixTemplate',
        related_name='hosts',
        verbose_name=_('Templates'),
    )
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=ZABBIX_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(blank=True, null=True)
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type', fk_field='assigned_object_id'
    )

    class Meta:
        ordering = (
            'server',
            'assigned_object_type',
            'assigned_object_id',
        )
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'
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
                    'assigned_object_type',
                    'assigned_object_id',
                ),
                name='%(app_label)s_%(class)s_server_assigned_object_unique',
                nulls_distinct=False,
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_assigned_object_not_null',
                condition=models.Q(assigned_object_type__isnull=False)
                & models.Q(assigned_object_id__isnull=False),
                violation_error_message=_('The assigned object cannot be null'),
            ),
        ]

    @classmethod
    def get_query_flags(cls):
        return {
            'selectHostGroups': 'extend',
            'selectInterfaces': 'extend',
            'selectParentTemplates': 'extend',
        }

    def __str__(self):
        if self.assigned_object_type and self.assigned_object_id:
            return f'{self.assigned_object.name}'
        return ''


class ZabbixHostInterface(JobsMixin, ZabbixID, PrimaryModel):
    host = models.ForeignKey(
        to=ZabbixHost,
        on_delete=models.CASCADE,
        related_name='interfaces',
        verbose_name=_('Host'),
    )
    type = models.CharField(
        choices=ZabbixHostInterfaceTypeChoices,
        max_length=10,
        verbose_name=_('Interface Type'),
    )
    connection = models.CharField(
        choices=ZabbixHostInterfaceConnectionChoices,
        max_length=3,
        verbose_name=_('Connect via'),
    )
    ip = models.ForeignKey(
        to=IPAddress,
        on_delete=models.CASCADE,
        related_name='zabbix_host_interfaces',
        verbose_name=_('IP Address'),
        blank=True,
        null=True,
    )
    dns = models.CharField(
        max_length=255,
        verbose_name=_('DNS Name'),
        blank=True,
        null=True,
    )
    port = models.PositiveIntegerField(
        verbose_name=_('Port'),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('host', 'type', 'connection', 'ip', 'id')
        verbose_name = 'Host Interface'
        verbose_name_plural = 'Host Interfaces'
        constraints = [
            models.UniqueConstraint(
                fields=('zid',),
                name='%(app_label)s_%(class)s_server_zid_unique',
            ),
        ]

    @classmethod
    def get_query_flags(cls):
        return {}

    @classmethod
    def get_zid_field_name(cls):
        return 'interfaceid'

    @classmethod
    def instantiate(cls, server, entry, key_field):
        try:
            host = ZabbixHost.objects.get(zid=entry.get('hostid'), server=server)
            return cls(host=host, zid=entry.get(key_field))
        except ZabbixHost.DoesNotExist:
            return None

    @classmethod
    def get_additional_filter_query_params(cls, server, entry):
        return {'host__server': server}

    def __str__(self):
        if self.host:
            return f'{self.host} ({self.type})'
        return ''


class ZabbixHostInterfaceSNMP(NetBoxModel):
    interface = models.OneToOneField(
        to=ZabbixHostInterface,
        on_delete=models.CASCADE,
        related_name='snmp',
        verbose_name=_('Interface'),
    )
    version = models.CharField(
        choices=ZabbixHostInterfaceSNMPVersionChoices,
        max_length=3,
        verbose_name=_('SNMP Version'),
    )
    community = models.CharField(
        max_length=255,
        verbose_name=_('Community String'),
        blank=True,
        null=True,
    )
    context_name = models.CharField(
        max_length=255,
        verbose_name=_('Security Name'),
        blank=True,
        null=True,
    )
    security_name = models.CharField(
        max_length=255,
        verbose_name=_('Security Name'),
        blank=True,
        null=True,
    )
    security_level = models.CharField(
        choices=ZabbixHostInterfaceSNMPSecurityChoices,
        max_length=15,
        verbose_name=_('SNMP Version'),
        blank=True,
        null=True,
    )
    auth_protocol = models.CharField(
        choices=ZabbixHostInterfaceSNMPAuthProtocolChoices,
        max_length=10,
        verbose_name=_('Authentication Protocol'),
        blank=True,
        null=True,
    )
    auth_passphrase = models.CharField(
        max_length=255,
        verbose_name=_('Authentication Passphrase'),
        blank=True,
        null=True,
    )
    priv_protocol = models.CharField(
        choices=ZabbixHostInterfaceSNMPPrivacyProtocolChoices,
        max_length=10,
        verbose_name=_('Authentication Protocol'),
        blank=True,
        null=True,
    )
    priv_passphrase = models.CharField(
        max_length=255,
        verbose_name=_('Authentication Passphrase'),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('interface',)
        verbose_name = 'Host Interface SNMP'
        verbose_name_plural = 'Host Interface SNMP'
        constraints = [
            models.UniqueConstraint(
                fields=('interface',),
                name='%(app_label)s_%(class)s_interface_unique',
            ),  # 1. If version is v1 or v2c: all except interface, version, community must be blank
            models.CheckConstraint(
                name='zabbixhostinterfacesnmp_v1_v2c_fields_blank',
                condition=(
                    models.Q(version__in=['v1', 'v2c'])
                    & models.Q(context_name__isnull=True)
                    & models.Q(context_name='')
                    & models.Q(security_name__isnull=True)
                    & models.Q(security_name='')
                    & models.Q(security_level__isnull=True)
                    & models.Q(security_level='')
                    & models.Q(auth_protocol__isnull=True)
                    & models.Q(auth_protocol='')
                    & models.Q(auth_passphrase__isnull=True)
                    & models.Q(auth_passphrase='')
                    & models.Q(priv_protocol__isnull=True)
                    & models.Q(priv_protocol='')
                    & models.Q(priv_passphrase__isnull=True)
                    & models.Q(priv_passphrase='')
                )
                | ~models.Q(version__in=['v1', 'v2c']),
            ),
            # 2. If version is v3: community must be blank, security_name and security_level must be set
            models.CheckConstraint(
                name='zabbixhostinterfacesnmp_v3_fields',
                condition=(
                    models.Q(version='v3')
                    & models.Q(community__isnull=True)
                    & models.Q(community='')
                    & models.Q(security_name__isnull=False)
                    & ~models.Q(security_name='')
                    & models.Q(security_level__isnull=False)
                    & ~models.Q(security_level='')
                )
                | ~models.Q(version='v3'),
            ),
            # 3, 4, 5. Security level logic
            models.CheckConstraint(
                name='zabbixhostinterfacesnmp_securitylevel_fields',
                condition=(
                    # noAuthnoPriv: all auth/priv fields blank
                    (
                        models.Q(security_level='noAuthnoPriv')
                        & models.Q(auth_protocol__isnull=True)
                        & models.Q(auth_protocol='')
                        & models.Q(auth_passphrase__isnull=True)
                        & models.Q(auth_passphrase='')
                        & models.Q(priv_protocol__isnull=True)
                        & models.Q(priv_protocol='')
                        & models.Q(priv_passphrase__isnull=True)
                        & models.Q(priv_passphrase='')
                    )
                    |
                    # authnoPriv: auth fields set, priv fields blank
                    (
                        models.Q(security_level='authNoPriv')
                        & models.Q(auth_protocol__isnull=False)
                        & ~models.Q(auth_protocol='')
                        & models.Q(auth_passphrase__isnull=False)
                        & ~models.Q(auth_passphrase='')
                        & models.Q(priv_protocol__isnull=True)
                        & models.Q(priv_protocol='')
                        & models.Q(priv_passphrase__isnull=True)
                        & models.Q(priv_passphrase='')
                    )
                    |
                    # authPriv: all auth/priv fields set
                    (
                        models.Q(security_level='authPriv')
                        & models.Q(auth_protocol__isnull=False)
                        & ~models.Q(auth_protocol='')
                        & models.Q(auth_passphrase__isnull=False)
                        & ~models.Q(auth_passphrase='')
                        & models.Q(priv_protocol__isnull=False)
                        & ~models.Q(priv_protocol='')
                        & models.Q(priv_passphrase__isnull=False)
                        & ~models.Q(priv_passphrase='')
                    )
                    |
                    # If security_level is null or blank, skip
                    models.Q(security_level__isnull=True)
                    | models.Q(security_level='')
                ),
            ),
        ]

    @classmethod
    def get_zid_field_name(cls):
        return f'interfaceid'

    def __str__(self):
        return f'{self.interface}'


class ZabbixHostTemplate(PrimaryModel):
    name = models.CharField(max_length=255)
    managed = models.BooleanField(
        verbose_name=_('Hosts managed'),
        default=True,
        help_text=_(
            'If unchecked, this template will not be used to create any new hosts.'
        ),
    )

    # Set Criteria
    templates = models.ManyToManyField(
        to='netbox_zabbix.ZabbixTemplate',
        related_name='host_templates',
        verbose_name=_('Templates'),
    )
    groups = models.ManyToManyField(
        to='netbox_zabbix.ZabbixHostGroup',
        related_name='host_templates',
        verbose_name=_('Host Groups'),
    )

    # Match Criteria
    regions = models.ManyToManyField(
        to='dcim.Region',
        related_name='host_templates',
        verbose_name=_('Regions'),
    )
    site_groups = models.ManyToManyField(
        to='dcim.SiteGroup',
        related_name='host_templates',
        verbose_name=_('Site Groups'),
    )
    sites = models.ManyToManyField(
        to='dcim.Site',
        related_name='host_templates',
        verbose_name=_('Sites'),
    )
    locations = models.ManyToManyField(
        to='dcim.Location',
        related_name='host_templates',
        verbose_name=_('Locations'),
    )
    device_types = models.ManyToManyField(
        to='dcim.DeviceType',
        related_name='host_templates',
        verbose_name=_('Device Types'),
    )
    roles = models.ManyToManyField(
        to='dcim.DeviceRole',
        related_name='host_templates',
        verbose_name=_('Roles'),
    )
    platforms = models.ManyToManyField(
        to='dcim.Platform',
        related_name='host_templates',
        verbose_name=_('Platforms'),
    )
    cluster_types = models.ManyToManyField(
        to='virtualization.ClusterType',
        related_name='host_templates',
        verbose_name=_('Cluster Types'),
    )
    cluster_groups = models.ManyToManyField(
        to='virtualization.ClusterGroup',
        related_name='host_templates',
        verbose_name=_('Cluster Groups'),
    )
    clusters = models.ManyToManyField(
        to='virtualization.Cluster',
        related_name='host_templates',
        verbose_name=_('Clusters'),
    )
    tenant_groups = models.ManyToManyField(
        to='tenancy.TenantGroup',
        related_name='host_templates',
        verbose_name=_('Tenant Groups'),
    )
    tenants = models.ManyToManyField(
        to='tenancy.Tenant',
        related_name='host_templates',
        verbose_name=_('Tenants'),
    )
    tags = models.ManyToManyField(
        to='extras.Tag',
    )

    class Meta:
        ordering = ('name', 'id')
        verbose_name = 'Zabbix Host Template'
        verbose_name_plural = 'Zabbix Host Templates'
        constraints = []

    def __str__(self):
        return f'{self.name}'
