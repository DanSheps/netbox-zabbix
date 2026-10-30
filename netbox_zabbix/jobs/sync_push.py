"""
Jobs for pushing NetBox Device and Virtual Machine changes to Zabbix.

This module implements push-sync operations that update Zabbix based on
changes made in NetBox.
"""
import logging
from datetime import datetime
from typing import Any

from django.contrib.contenttypes.models import ContentType
from zabbix_utils import ZabbixAPI

from dcim.models import Device
from netbox.config import get_config
from netbox.context_managers import event_tracking
from netbox.jobs import JobRunner, system_job
from netbox_zabbix.models import ZabbixHost
from virtualization.models import VirtualMachine

__all__ = (
    'SystemSyncNetBoxDeviceToZabbix',
    'SystemSyncNetBoxVirtualMachineToZabbix',
)

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


class PushSyncMixin:
    """Mixin for pushing NetBox changes to Zabbix."""

    @property
    def log(self):
        """Get logger instance - use instance logger if available (from JobRunner), else module logger."""
        return getattr(self, 'logger', logger)

    def _create_zabbix_api(self, server):
        """
        Create a ZabbixAPI connection for a specific Zabbix server.

        Args:
            server: ZabbixServer instance

        Returns:
            ZabbixAPI: Initialized ZabbixAPI connection, or None if failed
        """
        try:
            zabbix = ZabbixAPI(
                url=server.api_url,
                token=server.api_token,
                validate_certs=server.validate_certificates,
            )
            return zabbix
        except Exception as e:
            self.log.error(f'Failed to create ZabbixAPI connection for server {server.name}: {e}')
            return None


    def _get_interface_info(self, obj):
        """
        Extract interface information from a NetBox object.

        Args:
            obj: Device or VirtualMachine instance

        Returns:
            dict: Interface information (IP, SNMP data, etc.)
        """
        interface_data = {}

        try:
            # Get primary IP if available
            if hasattr(obj, 'primary_ip4'):
                primary_ip = obj.primary_ip4
                if primary_ip:
                    interface_data['ip'] = str(primary_ip.address.ip)

            # Get SNMP community if available (can be custom field or attribute)
            snmp_data = {}
            if hasattr(obj, 'custom_fields') and obj.custom_fields:
                if 'snmp_community' in obj.custom_fields:
                    snmp_data['community'] = obj.custom_fields['snmp_community']
                if 'snmp_version' in obj.custom_fields:
                    snmp_data['version'] = obj.custom_fields['snmp_version']

            if snmp_data:
                interface_data['snmp'] = snmp_data
        except Exception as e:
            self.log.warning(f'Error extracting interface info: {e}')

        return interface_data

    def push_device_to_zabbix(self, zabbix_host: ZabbixHost) -> bool:
        """
        Push NetBox Device changes to Zabbix Host using ZabbixAPI.

        Args:
            zabbix_host: Associated ZabbixHost instance

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the assigned device
            device = zabbix_host.assigned_object
            if not device or not isinstance(device, Device):
                self.log.error(f'ZabbixHost {zabbix_host.pk} has no assigned Device')
                return False

            server = zabbix_host.server
            if not server.enabled:
                self.log.warning(f'Server {server.name} is disabled, skipping sync')
                return False

            # Create ZabbixAPI connection with server-specific credentials
            zabbix = self._create_zabbix_api(server)
            if not zabbix:
                return False

            # Get interface information
            interface_info = self._get_interface_info(device)
            ip = interface_info.get('ip')
            snmp = interface_info.get('snmp', {})

            # Get existing host to verify it exists
            try:
                host_result = zabbix.host.get(hostids=[int(zabbix_host.zid)])  # type: ignore
                if not host_result:
                    self.log.error(f'Host {device.name} not found in Zabbix with ID {zabbix_host.zid}')
                    return False
            except Exception as e:
                self.log.error(f'Error retrieving host {device.name}: {e}')
                return False

            # Get current interface info
            try:
                interface_result = zabbix.hostinterface.get(hostids=[int(zabbix_host.zid)])  # type: ignore
                current_interface = interface_result[0] if interface_result else {}
            except Exception as e:
                self.log.error(f'Error retrieving interface for {device.name}: {e}')
                return False

            # Prepare host update data
            update_data: dict[str, Any] = {
                'hostid': str(zabbix_host.zid),
                'name': device.name,
            }

            # Add templates if any
            templates = list(zabbix_host.templates.all())
            if templates:
                update_data['templates'] = [{'templateid': str(t.zid)} for t in templates]

            # Add groups if any
            groups = list(zabbix_host.groups.all())
            if groups:
                update_data['groups'] = [{'groupid': str(g.zid)} for g in groups]

            # Update host basic info
            try:
                zabbix.host.update(**update_data)  # type: ignore
            except Exception as e:
                self.log.error(f'Error updating host {device.name}: {e}')
                return False

            # Update interface if needed
            if ip and current_interface:
                interface_id = current_interface.get('interfaceid')
                current_ip = current_interface.get('ip')
                current_snmp_version = current_interface.get('details', {}).get('version')

                if current_ip != ip or (snmp and current_snmp_version != snmp.get('version')):
                    self.log.info(f'Interface mismatch detected for {device.name}. Current IP: {current_ip}, Desired IP: {ip}')

                    interface_update = {
                        'interfaceid': interface_id,
                    }

                    if current_ip != ip:
                        interface_update['ip'] = ip

                    if snmp:
                        if 'details' not in interface_update:
                            interface_update['details'] = {}
                        for key, value in snmp.items():
                            interface_update['details'][key] = value

                    try:
                        zabbix.hostinterface.update(**interface_update)  # type: ignore
                        self.log.info(f'Updated interface for {device.name}')
                    except Exception as e:
                        self.log.warning(f'Error updating interface for {device.name}: {e}')
                        # Don't fail completely, host update succeeded

            self.log.info(f'Successfully pushed {device.name} to Zabbix')
            zabbix_host.last_synced = datetime.now()
            zabbix_host.save(update_fields=['last_synced'])
            return True

        except Exception as e:
            self.log.error(f'Error pushing device to Zabbix: {e}', exc_info=True)
            return False

    def push_virtual_machine_to_zabbix(self, zabbix_host: ZabbixHost) -> bool:
        """
        Push NetBox Virtual Machine changes to Zabbix Host using ZabbixAPI.

        Args:
            zabbix_host: Associated ZabbixHost instance

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the assigned VM
            vm = zabbix_host.assigned_object
            if not vm or not isinstance(vm, VirtualMachine):
                self.log.error(f'ZabbixHost {zabbix_host.pk} has no assigned VirtualMachine')
                return False

            server = zabbix_host.server
            if not server.enabled:
                self.log.warning(f'Server {server.name} is disabled, skipping sync')
                return False

            # Create ZabbixAPI connection with server-specific credentials
            zabbix = self._create_zabbix_api(server)
            if not zabbix:
                return False

            # Get interface information
            interface_info = self._get_interface_info(vm)
            ip = interface_info.get('ip')
            snmp = interface_info.get('snmp', {})

            # Get existing host to verify it exists
            try:
                host_result = zabbix.host.get(hostids=[int(zabbix_host.zid)])  # type: ignore
                if not host_result:
                    self.log.error(f'Host {vm.name} not found in Zabbix with ID {zabbix_host.zid}')
                    return False
            except Exception as e:
                self.log.error(f'Error retrieving host {vm.name}: {e}')
                return False

            # Get current interface info
            try:
                interface_result = zabbix.hostinterface.get(hostids=[int(zabbix_host.zid)])  # type: ignore
                current_interface = interface_result[0] if interface_result else {}
            except Exception as e:
                self.log.error(f'Error retrieving interface for {vm.name}: {e}')
                return False

            # Prepare host update data
            update_data: dict[str, Any] = {
                'hostid': str(zabbix_host.zid),
                'name': vm.name,
            }

            # Add templates if any
            templates = list(zabbix_host.templates.all())
            if templates:
                update_data['templates'] = [{'templateid': str(t.zid)} for t in templates]

            # Add groups if any
            groups = list(zabbix_host.groups.all())
            if groups:
                update_data['groups'] = [{'groupid': str(g.zid)} for g in groups]

            # Update host basic info
            try:
                zabbix.host.update(**update_data)  # type: ignore
            except Exception as e:
                self.log.error(f'Error updating host {vm.name}: {e}')
                return False

            # Update interface if needed
            if ip and current_interface:
                interface_id = current_interface.get('interfaceid')
                current_ip = current_interface.get('ip')
                current_snmp_version = current_interface.get('details', {}).get('version')

                if current_ip != ip or (snmp and current_snmp_version != snmp.get('version')):
                    self.log.info(f'Interface mismatch detected for {vm.name}. Current IP: {current_ip}, Desired IP: {ip}')

                    interface_update = {
                        'interfaceid': interface_id,
                    }

                    if current_ip != ip:
                        interface_update['ip'] = ip

                    if snmp:
                        if 'details' not in interface_update:
                            interface_update['details'] = {}
                        for key, value in snmp.items():
                            interface_update['details'][key] = value

                    try:
                        zabbix.hostinterface.update(**interface_update)  # type: ignore
                        self.log.info(f'Updated interface for {vm.name}')
                    except Exception as e:
                        self.log.warning(f'Error updating interface for {vm.name}: {e}')
                        # Don't fail completely, host update succeeded

            self.log.info(f'Successfully pushed {vm.name} to Zabbix')
            zabbix_host.last_synced = datetime.now()
            zabbix_host.save(update_fields=['last_synced'])
            return True

        except Exception as e:
            self.log.error(f'Error pushing virtual machine to Zabbix: {e}', exc_info=True)
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

        # Get Device ContentType
        device_ct = ContentType.objects.get_for_model(Device)

        # Get all ZabbixHost instances assigned to Devices
        zabbix_hosts = ZabbixHost.objects.filter(
            assigned_object_type=device_ct,
            server__isnull=False
        ).select_related('server')

        for zabbix_host in zabbix_hosts:
            try:
                if self.push_device_to_zabbix(zabbix_host):
                    synced_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                self.logger.error(f'Error syncing ZabbixHost {zabbix_host.pk}: {e}')
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

        # Get VirtualMachine ContentType
        vm_ct = ContentType.objects.get_for_model(VirtualMachine)

        # Get all ZabbixHost instances assigned to VirtualMachines
        zabbix_hosts = ZabbixHost.objects.filter(
            assigned_object_type=vm_ct,
            server__isnull=False
        ).select_related('server')

        for zabbix_host in zabbix_hosts:
            try:
                if self.push_virtual_machine_to_zabbix(zabbix_host):
                    synced_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                self.logger.error(f'Error syncing ZabbixHost {zabbix_host.pk}: {e}')
                failed_count += 1

        self.logger.info(f'Virtual Machine sync completed: {synced_count} synced, {failed_count} failed')

