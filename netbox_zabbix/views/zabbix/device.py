from netbox.views.generic import (
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    ObjectListView,
    BulkEditView,
    BulkDeleteView,
)
from netbox.ui import layout
from netbox.ui.panels import (
    CommentsPanel,
    CustomFieldsPanel,
    TagsPanel,
)
from utilities.views import register_model_view

from netbox_zabbix.models import (
    ZabbixDevice,
    ZabbixVirtualMachine,
)
from netbox_zabbix import filtersets, forms, tables


__all__ = (
    'ZabbixDeviceListView',
    'ZabbixDeviceView',
    'ZabbixDeviceEditView',
    'ZabbixDeviceDeleteView',
    'ZabbixDeviceBulkEditView',
    'ZabbixDeviceBulkDeleteView',
    'ZabbixVirtualMachineListView',
    'ZabbixVirtualMachineView',
    'ZabbixVirtualMachineEditView',
    'ZabbixVirtualMachineDeleteView',
    'ZabbixVirtualMachineBulkEditView',
    'ZabbixVirtualMachineBulkDeleteView',
)


# ZabbixDevice Views
@register_model_view(ZabbixDevice, name='list', path='', detail=False)
class ZabbixDeviceListView(ObjectListView):
    """List view for ZabbixDevice sync configurations."""
    queryset = ZabbixDevice.objects.all()
    filterset = filtersets.ZabbixDeviceFilterSet
    table = tables.ZabbixDeviceTable
    action_buttons = ('add',)


@register_model_view(ZabbixDevice)
class ZabbixDeviceView(ObjectView):
    """Detail view for ZabbixDevice sync configuration."""
    queryset = ZabbixDevice.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixDevice, name='add', detail=False)
@register_model_view(ZabbixDevice, name='edit')
class ZabbixDeviceEditView(ObjectEditView):
    """Edit view for ZabbixDevice sync configuration."""
    queryset = ZabbixDevice.objects.all()
    form = forms.ZabbixDeviceForm


@register_model_view(ZabbixDevice, name='delete')
class ZabbixDeviceDeleteView(ObjectDeleteView):
    """Delete view for ZabbixDevice sync configuration."""
    queryset = ZabbixDevice.objects.all()


@register_model_view(ZabbixDevice, name='bulk-edit', detail=False)
class ZabbixDeviceBulkEditView(BulkEditView):
    """Bulk edit view for ZabbixDevice."""
    queryset = ZabbixDevice.objects.all()
    filterset = filtersets.ZabbixDeviceFilterSet
    table = tables.ZabbixDeviceTable
    form = forms.ZabbixDeviceBulkEditForm


@register_model_view(ZabbixDevice, name='bulk-delete', detail=False)
class ZabbixDeviceBulkDeleteView(BulkDeleteView):
    """Bulk delete view for ZabbixDevice."""
    queryset = ZabbixDevice.objects.all()
    filterset = filtersets.ZabbixDeviceFilterSet
    table = tables.ZabbixDeviceTable


# ZabbixVirtualMachine Views
@register_model_view(ZabbixVirtualMachine, name='list', path='', detail=False)
class ZabbixVirtualMachineListView(ObjectListView):
    """List view for ZabbixVirtualMachine sync configurations."""
    queryset = ZabbixVirtualMachine.objects.all()
    filterset = filtersets.ZabbixVirtualMachineFilterSet
    table = tables.ZabbixVirtualMachineTable
    action_buttons = ('add',)


@register_model_view(ZabbixVirtualMachine)
class ZabbixVirtualMachineView(ObjectView):
    """Detail view for ZabbixVirtualMachine sync configuration."""
    queryset = ZabbixVirtualMachine.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            CustomFieldsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        right_panels=[],
    )


@register_model_view(ZabbixVirtualMachine, name='add', detail=False)
@register_model_view(ZabbixVirtualMachine, name='edit')
class ZabbixVirtualMachineEditView(ObjectEditView):
    """Edit view for ZabbixVirtualMachine sync configuration."""
    queryset = ZabbixVirtualMachine.objects.all()
    form = forms.ZabbixVirtualMachineForm


@register_model_view(ZabbixVirtualMachine, name='delete')
class ZabbixVirtualMachineDeleteView(ObjectDeleteView):
    """Delete view for ZabbixVirtualMachine sync configuration."""
    queryset = ZabbixVirtualMachine.objects.all()


@register_model_view(ZabbixVirtualMachine, name='bulk-edit', detail=False)
class ZabbixVirtualMachineBulkEditView(BulkEditView):
    """Bulk edit view for ZabbixVirtualMachine."""
    queryset = ZabbixVirtualMachine.objects.all()
    filterset = filtersets.ZabbixVirtualMachineFilterSet
    table = tables.ZabbixVirtualMachineTable
    form = forms.ZabbixVirtualMachineBulkEditForm


@register_model_view(ZabbixVirtualMachine, name='bulk-delete', detail=False)
class ZabbixVirtualMachineBulkDeleteView(BulkDeleteView):
    """Bulk delete view for ZabbixVirtualMachine."""
    queryset = ZabbixVirtualMachine.objects.all()
    filterset = filtersets.ZabbixVirtualMachineFilterSet
    table = tables.ZabbixVirtualMachineTable



