"""
Views for manual synchronization of Zabbix objects.

These views handle queuing of manual sync jobs for various Zabbix entity types.
"""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import View
from utilities.views import register_model_view, GetReturnURLMixin

from netbox_zabbix.jobs import (
    ManualSyncZabbixProxyGroups,
    ManualSyncZabbixProxies,
    ManualSyncZabbixHostGroups,
    ManualSyncZabbixTemplates,
    ManualSyncZabbixHost,
)
from netbox_zabbix.models import (
    ZabbixProxyGroup,
    ZabbixProxy,
    ZabbixHostGroup,
    ZabbixTemplate,
    ZabbixHost,
)

__all__ = (
    'ZabbixProxyGroupSyncView',
    'ZabbixProxySyncView',
    'ZabbixHostGroupSyncView',
    'ZabbixTemplateSyncView',
    'ZabbixHostSyncView',
)


class ManualSyncViewMixin:
    """
    Mixin for manual sync views that handles job queuing.
    Subclasses should define:
    - job_class: The job class to queue
    - model: The model being synced
    """

    job_class = None
    queryset = None
    template_name = 'netbox_zabbix/sync.html'

    def get(self, request, *args, **kwargs):
        """Display confirmation page for sync."""
        context = {
            'model_name': self.queryset.model._meta.verbose_name_plural,
            'title': f'Sync {self.queryset.model._meta.verbose_name_plural}',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Queue the manual sync job and redirect with success message."""
        if self.job_class:
            # Instantiate and enqueue the job
            self.job_class.enqueue(schedule_at=timezone.now())

            # Add success message
            messages.success(
                request,
                f'Sync job for {self.queryset.model._meta.verbose_name_plural} has been queued.',
            )

        # Redirect back to the list view
        return redirect(self.get_return_url(request))


@register_model_view(ZabbixProxyGroup, name='sync', path='sync', detail=False)
class ZabbixProxyGroupSyncView(ManualSyncViewMixin, GetReturnURLMixin, View):
    """Manual sync view for Zabbix Proxy Groups."""

    queryset = ZabbixProxyGroup.objects.all()
    job_class = ManualSyncZabbixProxyGroups


@register_model_view(ZabbixProxy, name='sync', path='sync', detail=False)
class ZabbixProxySyncView(ManualSyncViewMixin, GetReturnURLMixin, View):
    """Manual sync view for Zabbix Proxies."""

    queryset = ZabbixProxy.objects.all()
    job_class = ManualSyncZabbixProxies


@register_model_view(ZabbixHostGroup, name='sync', path='sync', detail=False)
class ZabbixHostGroupSyncView(ManualSyncViewMixin, GetReturnURLMixin, View):
    """Manual sync view for Zabbix Host Groups."""

    queryset = ZabbixHostGroup.objects.all()
    job_class = ManualSyncZabbixHostGroups


@register_model_view(ZabbixTemplate, name='sync', path='sync', detail=False)
class ZabbixTemplateSyncView(ManualSyncViewMixin, GetReturnURLMixin, View):
    """Manual sync view for Zabbix Templates."""

    queryset = ZabbixTemplate.objects.all()
    job_class = ManualSyncZabbixTemplates


@register_model_view(ZabbixHost, name='sync', path='sync', detail=False)
class ZabbixHostSyncView(ManualSyncViewMixin, GetReturnURLMixin, View):
    """Manual sync view for Zabbix Hosts."""

    queryset = ZabbixHost.objects.all()
    job_class = ManualSyncZabbixHost
