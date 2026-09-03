from dcim.models import (
    Region,
    SiteGroup,
    Site,
    Location,
    DeviceType,
    Platform,
    DeviceRole,
)
from netbox.views.generic import (
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    ObjectListView,
    BulkEditView,
    BulkDeleteView,
    BulkImportView,
    BulkRenameView,
    ObjectChildrenView,
)
from netbox.ui import actions, layout
from netbox.ui.panels import (
    CommentsPanel,
    ContextTablePanel,
    JSONPanel,
    NestedGroupObjectPanel,
    ObjectsTablePanel,
    OrganizationalObjectPanel,
    Panel,
    RelatedObjectsPanel,
    TemplatePanel,
)
from extras.ui.panels import CustomFieldsPanel, ImageAttachmentsPanel, TagsPanel
from utilities.views import register_model_view, ViewTab, GetRelatedModelsMixin

from netbox_zabbix.models import (
    ZabbixServer,
    ZabbixProxyGroup,
    ZabbixProxy,
    ZabbixHostGroup,
    ZabbixTemplate,
    ZabbixHost,
    ZabbixHostInterface,
    ZabbixHostTemplate,
)
from netbox_zabbix import filtersets, forms, tables
from netbox_zabbix.ui import (
    ZabbixHostGroupPanel,
    ZabbixHostPanel,
    ZabbixHostInterfacePanel,
    ZabbixManagedHostTemplatePanel,
    ZabbixHostSNMPInterfacePanel,
)

__all__ = (
    "ZabbixHostGroupListView",
    "ZabbixHostGroupView",
    "ZabbixHostGroupEditView",
    "ZabbixHostGroupDeleteView",
    # "ZabbixHostGroupBulkImportView",
    "ZabbixHostGroupBulkEditView",
    "ZabbixHostGroupBulkDeleteView",
    "ZabbixHostGroupBulkRenameView",
)

from virtualization.models import ClusterType, ClusterGroup, Cluster


@register_model_view(ZabbixHostGroup, name="list", path="", detail=False)
class ZabbixHostGroupListView(ObjectListView):
    queryset = ZabbixHostGroup.objects.all()

    filterset = filtersets.ZabbixHostGroupFilterSet
    filterset_form = None
    table = tables.ZabbixHostGroupTable
    action_buttons = ("add",)


@register_model_view(ZabbixHostGroup)
class ZabbixHostGroupView(ObjectView):
    queryset = ZabbixHostGroup.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixHostGroupPanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixHostGroup, name="add", detail=False)
@register_model_view(ZabbixHostGroup, name="edit")
class ZabbixHostGroupEditView(ObjectEditView):
    queryset = ZabbixHostGroup.objects.all()
    form = forms.ZabbixHostGroupForm


@register_model_view(ZabbixHostGroup, name="delete")
class ZabbixHostGroupDeleteView(ObjectDeleteView):
    queryset = ZabbixHostGroup.objects.all()


@register_model_view(ZabbixHostGroup, 'bulk_edit', path='edit', detail=False)
class ZabbixHostGroupBulkEditView(BulkEditView):
    queryset = ZabbixHostGroup.objects.all()
    filterset = filtersets.ZabbixHostGroupFilterSet
    table = tables.ZabbixHostGroupTable
    form = forms.ZabbixHostGroupBulkEditForm


@register_model_view(ZabbixHostGroup, 'bulk_rename', path='rename', detail=False)
class ZabbixHostGroupBulkRenameView(BulkRenameView):
    queryset = ZabbixHostGroup.objects.all()
    filterset = filtersets.ZabbixHostGroupFilterSet


@register_model_view(ZabbixHostGroup, 'bulk_delete', path='delete', detail=False)
class ZabbixHostGroupBulkDeleteView(BulkDeleteView):
    queryset = ZabbixHostGroup.objects.all()
    filterset = filtersets.ZabbixHostGroupFilterSet
    table = tables.ZabbixHostGroupTable


@register_model_view(ZabbixHost, name="list", path="", detail=False)
class ZabbixHostListView(ObjectListView):
    queryset = ZabbixHost.objects.all()

    filterset = filtersets.ZabbixHostFilterSet
    filterset_form = None
    table = tables.ZabbixHostTable
    action_buttons = ("add",)


@register_model_view(ZabbixHost)
class ZabbixHostView(ObjectView):
    queryset = ZabbixHost.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixHostPanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixHost, name="add", detail=False)
@register_model_view(ZabbixHost, name="edit")
class ZabbixHostEditView(ObjectEditView):
    queryset = ZabbixHost.objects.all()
    form = forms.ZabbixHostForm


@register_model_view(ZabbixHost, name="delete")
class ZabbixHostDeleteView(ObjectDeleteView):
    queryset = ZabbixHost.objects.all()


@register_model_view(ZabbixHost, 'bulk_edit', path='edit', detail=False)
class ZabbixHostBulkEditView(BulkEditView):
    queryset = ZabbixHost.objects.all()
    filterset = filtersets.ZabbixHostFilterSet
    table = tables.ZabbixHostTable
    form = forms.ZabbixHostBulkEditForm


@register_model_view(ZabbixHost, 'bulk_rename', path='rename', detail=False)
class ZabbixHostBulkRenameView(BulkRenameView):
    queryset = ZabbixHost.objects.all()
    filterset = filtersets.ZabbixHostFilterSet


@register_model_view(ZabbixHost, 'bulk_delete', path='delete', detail=False)
class ZabbixHostBulkDeleteView(BulkDeleteView):
    queryset = ZabbixHost.objects.all()
    filterset = filtersets.ZabbixHostFilterSet
    table = tables.ZabbixHostTable


@register_model_view(ZabbixHostInterface, name="list", path="", detail=False)
class ZabbixHostInterfaceListView(ObjectListView):
    queryset = ZabbixHostInterface.objects.all()

    filterset = filtersets.ZabbixHostInterfaceFilterSet
    filterset_form = None
    table = tables.ZabbixHostInterfaceTable
    action_buttons = ("add",)


@register_model_view(ZabbixHostInterface)
class ZabbixHostInterfaceView(ObjectView):
    queryset = ZabbixHostInterface.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixHostInterfacePanel(),
            ZabbixHostSNMPInterfacePanel(accessor='object.snmp'),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixHostInterface, name="add", detail=False)
@register_model_view(ZabbixHostInterface, name="edit")
class ZabbixHostInterfaceEditView(ObjectEditView):
    queryset = ZabbixHostInterface.objects.all()
    form = forms.ZabbixHostInterfaceForm


@register_model_view(ZabbixHostInterface, name="delete")
class ZabbixHostInterfaceDeleteView(ObjectDeleteView):
    queryset = ZabbixHostInterface.objects.all()


@register_model_view(ZabbixHostInterface, 'bulk_edit', path='edit', detail=False)
class ZabbixHostInterfaceBulkEditView(BulkEditView):
    queryset = ZabbixHostInterface.objects.all()
    filterset = filtersets.ZabbixHostInterfaceFilterSet
    table = tables.ZabbixHostInterfaceTable
    form = forms.ZabbixHostInterfaceBulkEditForm


@register_model_view(ZabbixHostInterface, 'bulk_rename', path='rename', detail=False)
class ZabbixHostInterfaceBulkRenameView(BulkRenameView):
    queryset = ZabbixHostInterface.objects.all()
    filterset = filtersets.ZabbixHostInterfaceFilterSet


@register_model_view(ZabbixHostInterface, 'bulk_delete', path='delete', detail=False)
class ZabbixHostInterfaceBulkDeleteView(BulkDeleteView):
    queryset = ZabbixHostInterface.objects.all()
    filterset = filtersets.ZabbixHostInterfaceFilterSet
    table = tables.ZabbixHostInterfaceTable


@register_model_view(ZabbixHostTemplate, name="list", path="", detail=False)
class ZabbixManagedHostTemplateListView(ObjectListView):
    queryset = ZabbixHostTemplate.objects.all()

    filterset = None
    filterset_form = None
    table = tables.ZabbixManagedHostTemplateTable
    action_buttons = ("add",)


@register_model_view(ZabbixHostTemplate)
class ZabbixManagedHostTemplateView(GetRelatedModelsMixin, ObjectView):
    queryset = ZabbixHostTemplate.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixManagedHostTemplatePanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[
            ObjectsTablePanel(
                'netbox_zabbix.ZabbixTemplate',
                filters={'host_template_id': lambda ctx: ctx['object'].pk},
                include_columns=['name', 'description'],
            ),
            ObjectsTablePanel(
                'netbox_zabbix.ZabbixHostGroup',
                filters={'host_template_id': lambda ctx: ctx['object'].pk},
                include_columns=['name', 'description'],
            ),
            RelatedObjectsPanel(),
        ],
    )

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(
                request,
                instance,
                omit=(),
                extra=(
                    (
                        Region.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        SiteGroup.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        Site.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        Location.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        DeviceType.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        DeviceRole.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        Platform.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        ClusterType.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        ClusterGroup.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                    (
                        Cluster.objects.restrict(request.user, 'view').filter(
                            host_templates__in=[instance]
                        ),
                        'host_template_id',
                    ),
                ),
            ),
        }


@register_model_view(ZabbixHostTemplate, name="add", detail=False)
@register_model_view(ZabbixHostTemplate, name="edit")
class ZabbixManagedHostTemplateEditView(ObjectEditView):
    queryset = ZabbixHostTemplate.objects.all()
    form = forms.ZabbixManagedHostTemplateForm


@register_model_view(ZabbixHostTemplate, name="delete")
class ZabbixManagedHostTemplateDeleteView(ObjectDeleteView):
    queryset = ZabbixHostTemplate.objects.all()
