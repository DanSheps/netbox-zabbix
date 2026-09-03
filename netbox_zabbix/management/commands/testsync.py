from django.core.management.base import BaseCommand

from netbox.context_managers import event_tracking
from netbox_zabbix.jobs.mixins import JobInstanceMixin
from netbox_zabbix.jobs.zabbix import (
    SyncZabbixSyncMixin,
    SystemSyncZabbixHost,
    SystemSyncZabbixHostInterface,
    SystemSyncZabbixHostGroups,
    SystemSyncZabbixProxyGroups,
    SystemSyncZabbixProxies,
    SystemSyncZabbixTemplates,
)
from netbox_zabbix.models import (
    ZabbixTemplate,
    ZabbixHostGroup,
    ZabbixProxyGroup,
    ZabbixProxy,
)


class Command(SyncZabbixSyncMixin, JobInstanceMixin, BaseCommand):
    help = "Test the Zabbix API"

    def handle(self, *args, **kwargs):
        with event_tracking(request=None):
            SystemSyncZabbixProxyGroups.enqueue(immediate=True)
            SystemSyncZabbixProxies.enqueue(immediate=True)
            SystemSyncZabbixTemplates.enqueue(immediate=True)
            SystemSyncZabbixHostGroups.enqueue(immediate=True)
            SystemSyncZabbixHost.enqueue(immediate=True)
            SystemSyncZabbixHostInterface.enqueue(immediate=True)
            pass
