from django import forms
from django.utils.translation import gettext as _

from dcim.models import (
    Device,
    VirtualChassis,
    VirtualDeviceContext,
    Region,
    SiteGroup,
    Location,
    Site,
    DeviceType,
    Platform,
    DeviceRole,
)
from extras.models import Tag
from netbox.forms import PrimaryModelForm
from netbox_zabbix.choices import (
    ZabbixHostInterfaceTypeChoices,
    ZabbixHostInterfaceConnectionChoices,
)
from netbox_zabbix.models.zabbix import ZabbixHostTemplate
from tenancy.models import TenantGroup, Tenant
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups

from netbox_zabbix.models import *

__all__ = (
    'ZabbixHostGroupForm',
    'ZabbixHostForm',
    'ZabbixHostInterfaceForm',
    'ZabbixManagedHostTemplateForm',
)

from virtualization.models import VirtualMachine, ClusterType, ClusterGroup, Cluster


class ZabbixHostGroupForm(PrimaryModelForm):

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'name',
            'description',
        ),
    )

    class Meta:
        model = ZabbixHostGroup
        fields = (
            'name',
            'description',
            'comments',
            'owner',
            'tags',
        )


class ZabbixHostForm(PrimaryModelForm):
    server = DynamicModelChoiceField(
        queryset=ZabbixServer.objects.all(),
        required=True,
        selector=True,
        label=_('Zabbix Server'),
    )
    proxy_group = DynamicModelChoiceField(
        queryset=ZabbixProxyGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Zabbix Proxy Group'),
    )
    proxy = DynamicModelChoiceField(
        queryset=ZabbixProxy.objects.all(),
        required=False,
        selector=True,
        label=_('Zabbix Proxy'),
    )
    templates = DynamicModelMultipleChoiceField(
        queryset=ZabbixTemplate.objects.all(),
        required=True,
        selector=True,
        label=_('Templates'),
    )
    groups = DynamicModelMultipleChoiceField(
        queryset=ZabbixHostGroup.objects.all(),
        required=True,
        selector=True,
        label=_('Host Groups'),
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    vdc = DynamicModelChoiceField(
        queryset=VirtualDeviceContext.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machine'),
    )
    vc = DynamicModelChoiceField(
        queryset=VirtualChassis.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machine'),
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machine'),
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'server',
            'templates',
        ),
        FieldSet(
            TabbedGroups(
                FieldSet('device', name=_('Device')),
                FieldSet('vc', name=_('Chassis')),
                FieldSet('vdc', name=_('VDC')),
                FieldSet(
                    'virtual_machine',
                    name=_('Virtualization'),
                ),
            ),
            'groups',
            name=_('Assigned Object'),
        ),
        FieldSet(
            'proxy_group',
            'proxy',
        ),
        FieldSet(
            'description',
        ),
    )

    class Meta:
        model = ZabbixHost
        fields = (
            'server',
            'templates',
            'proxy_group',
            'proxy',
            'device',
            'virtual_machine',
            'groups',
            'description',
            'comments',
            'owner',
            'tags',
        )

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is Device:
                initial['device'] = instance.assigned_object
            elif type(instance.assigned_object) is VirtualDeviceContext:
                initial['vdc'] = instance.assigned_object
            elif type(instance.assigned_object) is VirtualChassis:
                initial['vc'] = instance.assigned_object
            elif type(instance.assigned_object) is VirtualMachine:
                initial['virtual_machine'] = instance.assigned_object
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field
            for field in (
                'device',
                'virtual_machine',
                'vdc',
                'vc',
            )
            if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError(
                {
                    selected_objects[1]: _(
                        "A Zabbix Host can only be assigned to a single object."
                    )
                }
            )
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None

        filter = {selected_objects[0]: self.instance.assigned_object}
        if (
            self.Meta.model.objects.filter(**filter)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                {
                    selected_objects[0]: _(
                        "A Zabbix Host with this object already exists."
                    )
                }
            )


class ZabbixHostInterfaceForm(PrimaryModelForm):
    server = DynamicModelChoiceField(
        queryset=ZabbixHost.objects.all(),
        required=True,
        selector=True,
        label=_('Zabbix Host'),
    )
    type = forms.ChoiceField(
        choices=ZabbixHostInterfaceTypeChoices,
        required=True,
        label=_('Interface Type'),
    )
    connection = forms.ChoiceField(
        choices=ZabbixHostInterfaceConnectionChoices,
        required=True,
        label=_('Connection Type'),
    )

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'host',
            'type',
            'connection',
            'ip',
            'dns',
            'port',
            'description',
        ),
    )

    class Meta:
        model = ZabbixHostInterface
        fields = (
            'host',
            'type',
            'connection',
            'ip',
            'dns',
            'port',
            'description',
            'comments',
            'owner',
            'tags',
        )


class ZabbixManagedHostTemplateForm(PrimaryModelForm):
    name = forms.CharField(max_length=255)
    managed = forms.BooleanField()
    groups = DynamicModelMultipleChoiceField(
        queryset=ZabbixHostGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Host Groups'),
    )
    templates = DynamicModelMultipleChoiceField(
        queryset=ZabbixTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Templates'),
    )
    comments = CommentField()

    regions = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        selector=True,
        label=_('Regions'),
    )
    site_groups = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Site Groups'),
    )
    sites = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        selector=True,
        label=_('Sites'),
    )
    locations = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        selector=True,
        label=_('Locations'),
    )
    device_types = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label=_('Device Types'),
    )
    roles = DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(),
        required=False,
        selector=True,
        label=_('Roles'),
    )
    platforms = DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        selector=True,
        label=_('Platforms'),
    )
    cluster_types = DynamicModelMultipleChoiceField(
        queryset=ClusterType.objects.all(),
        required=False,
        selector=True,
        label=_('Cluster Types'),
    )
    cluster_groups = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Cluster Groups'),
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        selector=True,
        label=_('Cluster'),
    )
    tenant_groups = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant Groups'),
    )
    tenants = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenants'),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    comments = CommentField()

    fieldsets = (
        FieldSet(
            'name',
            'managed',
            'description',
        ),
        FieldSet('groups', 'templates', name=_('Assignment')),
        FieldSet(
            'regions',
            'site_groups',
            'sites',
            'locations',
            'device_types',
            'roles',
            'platforms',
            'cluster_types',
            'cluster_groups',
            'cluster',
            name=_('Matching Criteria'),
        ),
    )

    class Meta:
        model = ZabbixHostTemplate
        fields = (
            'name',
            'managed',
            'description',
            'groups',
            'templates',
            'regions',
            'site_groups',
            'sites',
            'locations',
            'device_types',
            'roles',
            'platforms',
            'cluster_types',
            'cluster_groups',
            'cluster',
            'tenant_groups',
            'tenants',
            'comments',
            'owner',
            'tags',
        )
