@register_model_view(ZabbixTemplateGroup, name="list", path="", detail=False)
class ZabbixTemplateGroupListView(ObjectListView):
    queryset = ZabbixTemplateGroup.objects.all()
    filterset = ZabbixTemplateGroupFilterSet
    filterset_form = ZabbixTemplateGroupFilterForm
    table = ZabbixTemplateGroupTable
    action_buttons = ("add",)


@register_model_view(ZabbixTemplateGroup)
class ZabbixTemplateGroupView(ObjectView):
    queryset = ZabbixTemplateGroup.objects.all()


@register_model_view(ZabbixTemplateGroup, name="add", detail=False)
@register_model_view(ZabbixTemplateGroup, name="edit")
class ZabbixTemplateGroupEditView(ObjectEditView):
    queryset = ZabbixTemplateGroup.objects.all()
    form = ZabbixTemplateGroupForm


@register_model_view(ZabbixTemplateGroup, name="delete")
class ZabbixTemplateGroupDeleteView(ObjectDeleteView):
    queryset = ZabbixTemplateGroup.objects.all()


@register_model_view(ZabbixTemplateGroup, name='bulk_import', detail=False)
class ZabbixTemplateGroupImportView(BulkImportView):
    queryset = ZabbixTemplateGroup.objects.all()
    model_form = ZabbixTemplateGroupBulkImportForm


@register_model_view(ZabbixTemplateGroup, name="bulk_edit", detail=False)
class ZabbixTemplateGroupBulkEditView(BulkEditView):
    filterset = ZabbixTemplateGroupFilterSet
    form = ZabbixTemplateGroupBulkEditForm
    queryset = ZabbixTemplateGroup.objects.all()
    table = ZabbixTemplateGroupTable


@register_model_view(ZabbixTemplateGroup, name="bulk_delete", detail=False)
class ZabbixTemplateGroupBulkDeleteView(BulkDeleteView):
    filterset = ZabbixTemplateGroupFilterSet
    queryset = ZabbixTemplateGroup.objects.all()
    table = ZabbixTemplateGroupTable
