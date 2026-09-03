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
from utilities.views import register_model_view, ViewTab


from netbox_zabbix.models import (
    ZabbixServer,
    ZabbixProxyGroup,
    ZabbixProxy,
    ZabbixHostGroup,
    ZabbixTemplate,
    ZabbixHost,
)
from netbox_zabbix import filtersets, forms, tables
from netbox_zabbix.ui import ZabbixServerPanel, ZabbixProxyGroupPanel, ZabbixProxyPanel

__all__ = (
    "ZabbixServerListView",
    "ZabbixServerView",
    "ZabbixServerEditView",
    "ZabbixServerDeleteView",
    # "ZabbixServerBulkImportView",
    "ZabbixServerBulkEditView",
    "ZabbixServerBulkDeleteView",
    "ZabbixServerBulkRenameView",
)


@register_model_view(ZabbixServer, name="list", path="", detail=False)
class ZabbixServerListView(ObjectListView):
    queryset = ZabbixServer.objects.all()

    filterset = filtersets.ZabbixServerFilterSet
    filterset_form = None
    table = tables.ZabbixServerTable
    action_buttons = ("add",)


@register_model_view(ZabbixServer)
class ZabbixServerView(ObjectView):
    queryset = ZabbixServer.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixServerPanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixServer, name="add", detail=False)
@register_model_view(ZabbixServer, name="edit")
class ZabbixServerEditView(ObjectEditView):
    queryset = ZabbixServer.objects.all()
    form = forms.ZabbixServerForm


@register_model_view(ZabbixServer, name="delete")
class ZabbixServerDeleteView(ObjectDeleteView):
    queryset = ZabbixServer.objects.all()


@register_model_view(ZabbixServer, 'bulk_edit', path='edit', detail=False)
class ZabbixServerBulkEditView(BulkEditView):
    queryset = ZabbixServer.objects.all()
    filterset = filtersets.ZabbixServerFilterSet
    table = tables.ZabbixServerTable
    form = forms.ZabbixServerBulkEditForm


@register_model_view(ZabbixServer, 'bulk_rename', path='rename', detail=False)
class ZabbixServerBulkRenameView(BulkRenameView):
    queryset = ZabbixServer.objects.all()
    filterset = filtersets.ZabbixServerFilterSet


@register_model_view(ZabbixServer, 'bulk_delete', path='delete', detail=False)
class ZabbixServerBulkDeleteView(BulkDeleteView):
    queryset = ZabbixServer.objects.all()
    filterset = filtersets.ZabbixServerFilterSet
    table = tables.ZabbixServerTable


@register_model_view(ZabbixServer, name='host-groups')
class ZabbixServerHostGroupListView(ObjectChildrenView):
    queryset = ZabbixServer.objects.all()
    child_model = ZabbixHostGroup
    table = tables.ZabbixHostGroupTable
    filterset = filtersets.ZabbixHostGroupFilterSet
    filterset_form = forms.ZabbixHostGroupFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Host Groups',
        badge=lambda obj: ZabbixServerHostGroupListView.child_model.objects.filter(
            server=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(server=parent)


@register_model_view(ZabbixServer, name='templates')
class ZabbixServerTemplateListView(ObjectChildrenView):
    queryset = ZabbixServer.objects.all()
    child_model = ZabbixTemplate
    table = tables.ZabbixTemplateTable
    filterset = filtersets.ZabbixTemplateFilterSet
    filterset_form = forms.ZabbixTemplateFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Templates',
        badge=lambda obj: ZabbixServerTemplateListView.child_model.objects.filter(
            server=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(server=parent)


@register_model_view(ZabbixProxyGroup, name="list", path="", detail=False)
class ZabbixProxyGroupListView(ObjectListView):
    queryset = ZabbixProxyGroup.objects.all()

    filterset = filtersets.ZabbixProxyGroupFilterSet
    filterset_form = None
    table = tables.ZabbixProxyGroupTable
    action_buttons = ("add",)


@register_model_view(ZabbixProxyGroup)
class ZabbixProxyGroupView(ObjectView):
    queryset = ZabbixProxyGroup.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixProxyGroupPanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixProxyGroup, name="add", detail=False)
@register_model_view(ZabbixProxyGroup, name="edit")
class ZabbixProxyGroupEditView(ObjectEditView):
    queryset = ZabbixProxyGroup.objects.all()
    form = forms.ZabbixProxyGroupForm


@register_model_view(ZabbixProxyGroup, name="delete")
class ZabbixProxyGroupDeleteView(ObjectDeleteView):
    queryset = ZabbixProxyGroup.objects.all()


@register_model_view(ZabbixProxyGroup, 'bulk_edit', path='edit', detail=False)
class ZabbixProxyGroupBulkEditView(BulkEditView):
    queryset = ZabbixProxyGroup.objects.all()
    filterset = filtersets.ZabbixProxyGroupFilterSet
    table = tables.ZabbixProxyGroupTable
    form = forms.ZabbixProxyGroupBulkEditForm


@register_model_view(ZabbixProxyGroup, 'bulk_rename', path='rename', detail=False)
class ZabbixProxyGroupBulkRenameView(BulkRenameView):
    queryset = ZabbixProxyGroup.objects.all()
    filterset = filtersets.ZabbixProxyGroupFilterSet


@register_model_view(ZabbixProxyGroup, 'bulk_delete', path='delete', detail=False)
class ZabbixProxyGroupBulkDeleteView(BulkDeleteView):
    queryset = ZabbixProxyGroup.objects.all()
    filterset = filtersets.ZabbixProxyGroupFilterSet
    table = tables.ZabbixProxyGroupTable


@register_model_view(ZabbixProxyGroup, name='host-groups')
class ZabbixProxyGroupHostGroupListView(ObjectChildrenView):
    queryset = ZabbixProxyGroup.objects.all()
    child_model = ZabbixHostGroup
    table = tables.ZabbixHostGroupTable
    filterset = filtersets.ZabbixHostGroupFilterSet
    filterset_form = forms.ZabbixHostGroupFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Host Groups',
        badge=lambda obj: ZabbixProxyGroupHostGroupListView.child_model.objects.filter(
            server=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(server=parent)


@register_model_view(ZabbixProxyGroup, name='templates')
class ZabbixProxyGroupTemplateListView(ObjectChildrenView):
    queryset = ZabbixProxyGroup.objects.all()
    child_model = ZabbixTemplate
    table = tables.ZabbixTemplateTable
    filterset = filtersets.ZabbixTemplateFilterSet
    filterset_form = forms.ZabbixTemplateFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Templates',
        badge=lambda obj: ZabbixProxyGroupTemplateListView.child_model.objects.filter(
            server=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(server=parent)


@register_model_view(ZabbixProxy, name="list", path="", detail=False)
class ZabbixProxyListView(ObjectListView):
    queryset = ZabbixProxy.objects.all()

    filterset = filtersets.ZabbixProxyFilterSet
    filterset_form = None
    table = tables.ZabbixProxyTable
    action_buttons = ("add",)


@register_model_view(ZabbixProxy)
class ZabbixProxyView(ObjectView):
    queryset = ZabbixProxy.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixProxyPanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixProxy, name="add", detail=False)
@register_model_view(ZabbixProxy, name="edit")
class ZabbixProxyEditView(ObjectEditView):
    queryset = ZabbixProxy.objects.all()
    form = forms.ZabbixProxyForm


@register_model_view(ZabbixProxy, name="delete")
class ZabbixProxyDeleteView(ObjectDeleteView):
    queryset = ZabbixProxy.objects.all()


@register_model_view(ZabbixProxy, 'bulk_edit', path='edit', detail=False)
class ZabbixProxyBulkEditView(BulkEditView):
    queryset = ZabbixProxy.objects.all()
    filterset = filtersets.ZabbixProxyFilterSet
    table = tables.ZabbixProxyTable
    form = forms.ZabbixProxyBulkEditForm


@register_model_view(ZabbixProxy, 'bulk_rename', path='rename', detail=False)
class ZabbixProxyBulkRenameView(BulkRenameView):
    queryset = ZabbixProxy.objects.all()
    filterset = filtersets.ZabbixProxyFilterSet


@register_model_view(ZabbixProxy, 'bulk_delete', path='delete', detail=False)
class ZabbixProxyBulkDeleteView(BulkDeleteView):
    queryset = ZabbixProxy.objects.all()
    filterset = filtersets.ZabbixProxyFilterSet
    table = tables.ZabbixProxyTable


@register_model_view(ZabbixProxy, name='host-groups')
class ZabbixProxyHostGroupListView(ObjectChildrenView):
    queryset = ZabbixProxy.objects.all()
    child_model = ZabbixHostGroup
    table = tables.ZabbixHostGroupTable
    filterset = filtersets.ZabbixHostGroupFilterSet
    filterset_form = forms.ZabbixHostGroupFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Host Groups',
        badge=lambda obj: ZabbixProxyHostGroupListView.child_model.objects.filter(
            server=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(server=parent)


@register_model_view(ZabbixProxy, name='templates')
class ZabbixProxyTemplateListView(ObjectChildrenView):
    queryset = ZabbixProxy.objects.all()
    child_model = ZabbixTemplate
    table = tables.ZabbixTemplateTable
    filterset = filtersets.ZabbixTemplateFilterSet
    filterset_form = forms.ZabbixTemplateFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Templates',
        badge=lambda obj: ZabbixProxyTemplateListView.child_model.objects.filter(
            server=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(server=parent)
