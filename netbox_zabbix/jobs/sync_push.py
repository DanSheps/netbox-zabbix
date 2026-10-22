"""
Jobs for pushing NetBox Device and Virtual Machine changes to Zabbix.

This module implements push-sync operations that update Zabbix based on
changes made in NetBox.
"""
import logging
from datetime import datetime

from django.db import models
from zabbix_utils import ZabbixAPI

from dcim.models import Device
from netbox.config import get_config
from netbox.context_managers import event_tracking
from netbox.jobs import JobRunner, system_job
from netbox_zabbix.models import (
    ZabbixServer,
    ZabbixHost,
    ZabbixDevice,
    ZabbixVirtualMachine,
)
from virtualization.models import VirtualMachine

__all__ = (
    'SystemSyncNetBoxDeviceToZabbix',
    'SystemSyncNetBoxVirtualMachineToZabbix',
)

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


class PushSyncMixin:
    """Mixin for pushing NetBox changes to Zabbix."""

    def push_device_to_zabbix(self, device: Device, zabbix_host: ZabbixHost) -> bool:
        """
        Push NetBox Device changes to Zabbix Host.

        Args:
            device: NetBox Device instance
            zabbix_host: Associated ZabbixHost instance

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            server = zabbix_host.server
            zabbix = ZabbixAPI(
                url=server.api_url,
                token=server.api_token,
                validate_certs=server.validate_certificates,
            )

            # Prepare host data for update
            host_data = {
                'hostid': str(zabbix_host.zid),
                'name': device.name,
                'description': device.comments or '',
                'status': 0 if device.status == 'active' else 1,
            }

            # Update host in Zabbix
            result = zabbix.host.update(**host_data)

            if result:
                self.logger.info(f'Successfully pushed {device.name} to Zabbix')
                return True
            else:
                self.logger.error(f'Failed to push {device.name} to Zabbix')
                return False

        except Exception as e:
            self.logger.error(f'Error pushing device {device.name} to Zabbix: {e}')
            return False

    def push_virtual_machine_to_zabbix(self, vm: VirtualMachine, zabbix_host: ZabbixHost) -> bool:
        """
        Push NetBox Virtual Machine changes to Zabbix Host.

        Args:
            vm: NetBox VirtualMachine instance
            zabbix_host: Associated ZabbixHost instance

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            server = zabbix_host.server
            zabbix = ZabbixAPI(
                url=server.api_url,
                token=server.api_token,
                validate_certs=server.validate_certificates,
            )

            # Prepare host data for update
            host_data = {
                'hostid': str(zabbix_host.zid),
                'name': vm.name,
                'description': vm.comments or '',
                'status': 0 if vm.status == 'active' else 1,
            }

            # Update host in Zabbix
            result = zabbix.host.update(**host_data)

            if result:
                self.logger.info(f'Successfully pushed {vm.name} to Zabbix')
                return True
            else:
                self.logger.error(f'Failed to push {vm.name} to Zabbix')
                return False

        except Exception as e:
            self.logger.error(f'Error pushing virtual machine {vm.name} to Zabbix: {e}')
            return False


@system_job(interval=1440)
class SystemSyncNetBoxDeviceToZabbix(PushSyncMixin, JobRunner):
    """System job to sync NetBox Devices to Zabbix."""

    def run(self, data=None, commit=True, *args, **kwargs):
        """Run the sync job."""
        if get_config().DEBUG:
            self.logger.info("DEBUG mode enabled, Skipping")
            return

        with event_tracking(request=None):
            self.sync_devices()

    def sync_devices(self):
        """Sync all enabled device syncs to Zabbix."""
        synced_count = 0
        failed_count = 0

        # Get all enabled device syncs
        device_syncs = ZabbixDevice.objects.filter(
            sync_enabled=True,
            zabbix_host__isnull=False
        )

        for device_sync in device_syncs:
            try:
                if self.push_device_to_zabbix(device_sync.device, device_sync.zabbix_host):
                    device_sync.last_synced = datetime.now()
                    device_sync.save(update_fields=['last_synced'])
                    synced_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                self.logger.error(f'Error syncing device {device_sync.device.name}: {e}')
                failed_count += 1

        self.logger.info(f'Device sync completed: {synced_count} synced, {failed_count} failed')


@system_job(interval=1440)
class SystemSyncNetBoxVirtualMachineToZabbix(PushSyncMixin, JobRunner):
    """System job to sync NetBox Virtual Machines to Zabbix."""

    def run(self, data=None, commit=True, *args, **kwargs):
        """Run the sync job."""
        if get_config().DEBUG:
            self.logger.info("DEBUG mode enabled, Skipping")
            return

        with event_tracking(request=None):
            self.sync_virtual_machines()

    def sync_virtual_machines(self):
        """Sync all enabled VM syncs to Zabbix."""
        synced_count = 0
        failed_count = 0

        # Get all enabled VM syncs
        vm_syncs = ZabbixVirtualMachine.objects.filter(
            sync_enabled=True,
            zabbix_host__isnull=False
        )

        for vm_sync in vm_syncs:
            try:
                if self.push_virtual_machine_to_zabbix(vm_sync.virtual_machine, vm_sync.zabbix_host):
                    vm_sync.last_synced = datetime.now()
                    vm_sync.save(update_fields=['last_synced'])
                    synced_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                self.logger.error(f'Error syncing virtual machine {vm_sync.virtual_machine.name}: {e}')
                failed_count += 1

        self.logger.info(f'Virtual Machine sync completed: {synced_count} synced, {failed_count} failed')

