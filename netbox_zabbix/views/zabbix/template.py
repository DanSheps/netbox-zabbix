from netbox.views.generic import (
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    ObjectListView,
    BulkEditView,
    BulkDeleteView,
    BulkImportView,
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
from extras.ui.panels import CustomFieldsPanel, TagsPanel
from netbox_zabbix.ui import ZabbixTemplatePanel
from utilities.views import register_model_view

from netbox_zabbix.forms import ZabbixTemplateForm, ZabbixTemplateFilterForm, ZabbixTemplateBulkEditForm
from netbox_zabbix.models import ZabbixTemplate
from netbox_zabbix.tables import ZabbixTemplateTable
from netbox_zabbix.filtersets import ZabbixTemplateFilterSet


__all__ = (
    "ZabbixTemplateListView",
    "ZabbixTemplateView",
    "ZabbixTemplateEditView",
    "ZabbixTemplateDeleteView",
    "ZabbixTemplateBulkEditView",
    "ZabbixTemplateBulkDeleteView",
)


@register_model_view(ZabbixTemplate, name="list", path="", detail=False)
class ZabbixTemplateListView(ObjectListView):
    queryset = ZabbixTemplate.objects.all()

    filterset = ZabbixTemplateFilterSet
    filterset_form = ZabbixTemplateFilterForm
    table = ZabbixTemplateTable
    action_buttons = ("add",)


@register_model_view(ZabbixTemplate)
class ZabbixTemplateView(ObjectView):
    queryset = ZabbixTemplate.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            ZabbixTemplatePanel(),
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixTemplate, name="add", detail=False)
@register_model_view(ZabbixTemplate, name="edit")
class ZabbixTemplateEditView(ObjectEditView):
    queryset = ZabbixTemplate.objects.all()
    form = ZabbixTemplateForm


@register_model_view(ZabbixTemplate, name="delete")
class ZabbixTemplateDeleteView(ObjectDeleteView):
    queryset = ZabbixTemplate.objects.all()


#@register_model_view(ZabbixTemplate, name='bulk_import', detail=False)
#class ZabbixTemplateImportView(BulkImportView):
#    queryset = ZabbixTemplate.objects.all()
#    model_form = ZabbixTemplateBulkImportForm


@register_model_view(ZabbixTemplate, name="bulk_edit", detail=False)
class ZabbixTemplateBulkEditView(BulkEditView):
    filterset = ZabbixTemplateFilterSet
    form = ZabbixTemplateBulkEditForm
    queryset = ZabbixTemplate.objects.all()
    table = ZabbixTemplateTable


@register_model_view(ZabbixTemplate, name="bulk_delete", detail=False)
class ZabbixTemplateBulkDeleteView(BulkDeleteView):
    filterset = ZabbixTemplateFilterSet
    queryset = ZabbixTemplate.objects.all()
    table = ZabbixTemplateTable


