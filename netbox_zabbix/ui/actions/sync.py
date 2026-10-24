from django.utils.translation import gettext_lazy as _
from netbox.object_actions import ObjectAction


class SyncObject(ObjectAction):
    """
    Sync the object.
    """

    name = 'sync'
    label = _('Sync')
    permissions_required = {'add'}
    template_name = 'netbox_zabbix/ui/buttons/sync.html'
