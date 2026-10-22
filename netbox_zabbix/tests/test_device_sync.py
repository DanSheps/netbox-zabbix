"""
Unit tests for netbox-zabbix plugin device sync functionality.
"""
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, MagicMock

from dcim.models import Device, DeviceType, Manufacturer, Site
from virtualization.models import VirtualMachine, Cluster, ClusterType, ClusterGroup

from netbox_zabbix.models import (
    ZabbixServer,
    ZabbixDevice,
    ZabbixVirtualMachine,
    ZabbixHost,
    ZabbixHostGroup,
)


class ZabbixDeviceModelTests(TestCase):
    """Tests for ZabbixDevice model."""

    def setUp(self):
        """Set up test data."""
        # Create required objects
        self.site = Site.objects.create(name='Test Site', slug='test-site')
        self.manufacturer = Manufacturer.objects.create(name='Test Mfg', slug='test-mfg')
        self.device_type = DeviceType.objects.create(
            manufacturer=self.manufacturer,
            model='Test Model',
            slug='test-model'
        )

        # Create Device
        self.device = Device.objects.create(
            name='test-device-01',
            site=self.site,
            device_type=self.device_type,
            status='active'
        )

        # Create Zabbix Server and Host
        self.zabbix_server = ZabbixServer.objects.create(
            name='Test Server',
            api_url='http://zabbix.example.com/api_jsonrpc.php',
            api_token='test-token'
        )

        self.zabbix_host = ZabbixHost.objects.create(
            name='test-zabbix-host',
            hostname='test-zabbix-host',
            server=self.zabbix_server,
            zid=10001
        )

    def test_create_zabbix_device(self):
        """Test creating a ZabbixDevice."""
        device_sync = ZabbixDevice.objects.create(
            device=self.device,
            zabbix_host=self.zabbix_host,
            zabbix_id=10001,
            sync_enabled=True,
            description='Test device sync'
        )

        self.assertEqual(device_sync.device, self.device)
        self.assertEqual(device_sync.zabbix_host, self.zabbix_host)
        self.assertTrue(device_sync.sync_enabled)
        self.assertEqual(str(device_sync), 'test-device-01')

    def test_zabbix_device_last_synced(self):
        """Test last_synced timestamp."""
        device_sync = ZabbixDevice.objects.create(
            device=self.device,
            zabbix_host=self.zabbix_host,
            sync_enabled=True
        )

        self.assertIsNone(device_sync.last_synced)

        now = timezone.now()
        device_sync.last_synced = now
        device_sync.save()

        device_sync.refresh_from_db()
        self.assertIsNotNone(device_sync.last_synced)

    def test_zabbix_device_unique_device(self):
        """Test that device can only have one sync configuration."""
        ZabbixDevice.objects.create(
            device=self.device,
            zabbix_host=self.zabbix_host,
            sync_enabled=True
        )

        # Try to create another sync for the same device
        with self.assertRaises(Exception):
            ZabbixDevice.objects.create(
                device=self.device,
                zabbix_host=self.zabbix_host,
                sync_enabled=False
            )


class ZabbixVirtualMachineModelTests(TestCase):
    """Tests for ZabbixVirtualMachine model."""

    def setUp(self):
        """Set up test data."""
        # Create Cluster
        cluster_type = ClusterType.objects.create(name='Test Type', slug='test-type')
        cluster_group = ClusterGroup.objects.create(name='Test Group', slug='test-group')
        self.cluster = Cluster.objects.create(
            name='test-cluster',
            type=cluster_type,
            group=cluster_group
        )

        # Create Virtual Machine
        self.vm = VirtualMachine.objects.create(
            name='test-vm-01',
            cluster=self.cluster,
            status='active'
        )

        # Create Zabbix Server and Host
        self.zabbix_server = ZabbixServer.objects.create(
            name='Test Server',
            api_url='http://zabbix.example.com/api_jsonrpc.php',
            api_token='test-token'
        )

        self.zabbix_host = ZabbixHost.objects.create(
            name='test-zabbix-vm-host',
            hostname='test-zabbix-vm-host',
            server=self.zabbix_server,
            zid=10002
        )

    def test_create_zabbix_virtual_machine(self):
        """Test creating a ZabbixVirtualMachine."""
        vm_sync = ZabbixVirtualMachine.objects.create(
            virtual_machine=self.vm,
            zabbix_host=self.zabbix_host,
            zabbix_id=10002,
            sync_enabled=True,
            description='Test VM sync'
        )

        self.assertEqual(vm_sync.virtual_machine, self.vm)
        self.assertEqual(vm_sync.zabbix_host, self.zabbix_host)
        self.assertTrue(vm_sync.sync_enabled)
        self.assertEqual(str(vm_sync), 'test-vm-01')

    def test_zabbix_vm_last_synced(self):
        """Test last_synced timestamp."""
        vm_sync = ZabbixVirtualMachine.objects.create(
            virtual_machine=self.vm,
            zabbix_host=self.zabbix_host,
            sync_enabled=True
        )

        self.assertIsNone(vm_sync.last_synced)

        now = timezone.now()
        vm_sync.last_synced = now
        vm_sync.save()

        vm_sync.refresh_from_db()
        self.assertIsNotNone(vm_sync.last_synced)


class ZabbixDeviceFormTests(TestCase):
    """Tests for ZabbixDevice form."""

    def setUp(self):
        """Set up test data."""
        from netbox_zabbix.forms import ZabbixDeviceForm

        self.form_class = ZabbixDeviceForm

        # Create Device
        site = Site.objects.create(name='Test Site', slug='test-site')
        manufacturer = Manufacturer.objects.create(name='Test Mfg', slug='test-mfg')
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model='Test Model',
            slug='test-model'
        )
        self.device = Device.objects.create(
            name='test-device-01',
            site=site,
            device_type=device_type
        )

        # Create Zabbix Host
        zabbix_server = ZabbixServer.objects.create(
            name='Test Server',
            api_url='http://zabbix.example.com/api_jsonrpc.php',
            api_token='test-token'
        )
        self.zabbix_host = ZabbixHost.objects.create(
            name='test-zabbix-host',
            hostname='test-zabbix-host',
            server=zabbix_server,
            zid=10001
        )

    def test_form_valid(self):
        """Test form with valid data."""
        form_data = {
            'device': self.device.pk,
            'zabbix_host': self.zabbix_host.pk,
            'sync_enabled': True,
            'description': 'Test',
        }
        form = self.form_class(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_required_fields(self):
        """Test form with missing required fields."""
        form_data = {
            'device': '',
            'zabbix_host': '',
        }
        form = self.form_class(data=form_data)
        self.assertFalse(form.is_valid())


class ZabbixVirtualMachineFormTests(TestCase):
    """Tests for ZabbixVirtualMachine form."""

    def setUp(self):
        """Set up test data."""
        from netbox_zabbix.forms import ZabbixVirtualMachineForm

        self.form_class = ZabbixVirtualMachineForm

        # Create Virtual Machine
        cluster_type = ClusterType.objects.create(name='Test Type', slug='test-type')
        cluster_group = ClusterGroup.objects.create(name='Test Group', slug='test-group')
        cluster = Cluster.objects.create(
            name='test-cluster',
            type=cluster_type,
            group=cluster_group
        )
        self.vm = VirtualMachine.objects.create(
            name='test-vm-01',
            cluster=cluster
        )

        # Create Zabbix Host
        zabbix_server = ZabbixServer.objects.create(
            name='Test Server',
            api_url='http://zabbix.example.com/api_jsonrpc.php',
            api_token='test-token'
        )
        self.zabbix_host = ZabbixHost.objects.create(
            name='test-zabbix-host',
            hostname='test-zabbix-host',
            server=zabbix_server,
            zid=10002
        )

    def test_form_valid(self):
        """Test form with valid data."""
        form_data = {
            'virtual_machine': self.vm.pk,
            'zabbix_host': self.zabbix_host.pk,
            'sync_enabled': True,
            'description': 'Test',
        }
        form = self.form_class(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_required_fields(self):
        """Test form with missing required fields."""
        form_data = {
            'virtual_machine': '',
            'zabbix_host': '',
        }
        form = self.form_class(data=form_data)
        self.assertFalse(form.is_valid())


class ZabbixDeviceAPITests(TestCase):
    """Tests for ZabbixDevice API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create Device
        site = Site.objects.create(name='Test Site', slug='test-site')
        manufacturer = Manufacturer.objects.create(name='Test Mfg', slug='test-mfg')
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model='Test Model',
            slug='test-model'
        )
        self.device = Device.objects.create(
            name='test-device-01',
            site=site,
            device_type=device_type
        )

        # Create Zabbix Host
        zabbix_server = ZabbixServer.objects.create(
            name='Test Server',
            api_url='http://zabbix.example.com/api_jsonrpc.php',
            api_token='test-token'
        )
        self.zabbix_host = ZabbixHost.objects.create(
            name='test-zabbix-host',
            hostname='test-zabbix-host',
            server=zabbix_server,
            zid=10001
        )

        # Create ZabbixDevice
        self.zabbix_device = ZabbixDevice.objects.create(
            device=self.device,
            zabbix_host=self.zabbix_host,
            sync_enabled=True
        )

    def test_list_zabbix_devices(self):
        """Test listing ZabbixDevice via API."""
        from rest_framework.test import APIRequestFactory
        from netbox_zabbix.api.views import ZabbixDeviceViewSet

        factory = APIRequestFactory()
        request = factory.get('/api/plugins/zabbix/zabbix-devices/')
        view = ZabbixDeviceViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_retrieve_zabbix_device(self):
        """Test retrieving a single ZabbixDevice via API."""
        from rest_framework.test import APIRequestFactory
        from netbox_zabbix.api.views import ZabbixDeviceViewSet

        factory = APIRequestFactory()
        request = factory.get(f'/api/plugins/zabbix/zabbix-devices/{self.zabbix_device.pk}/')
        view = ZabbixDeviceViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.zabbix_device.pk)

        self.assertEqual(response.status_code, 200)


class ZabbixPushSyncJobTests(TestCase):
    """Tests for push sync jobs."""

    def setUp(self):
        """Set up test data."""
        # Create Device
        site = Site.objects.create(name='Test Site', slug='test-site')
        manufacturer = Manufacturer.objects.create(name='Test Mfg', slug='test-mfg')
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model='Test Model',
            slug='test-model'
        )
        self.device = Device.objects.create(
            name='test-device-01',
            site=site,
            device_type=device_type,
            status='active'
        )

        # Create Zabbix Server and Host
        self.zabbix_server = ZabbixServer.objects.create(
            name='Test Server',
            api_url='http://zabbix.example.com/api_jsonrpc.php',
            api_token='test-token'
        )
        self.zabbix_host = ZabbixHost.objects.create(
            name='test-zabbix-host',
            hostname='test-zabbix-host',
            server=self.zabbix_server,
            zid=10001
        )

        # Create ZabbixDevice with sync enabled
        self.zabbix_device = ZabbixDevice.objects.create(
            device=self.device,
            zabbix_host=self.zabbix_host,
            sync_enabled=True
        )

    @patch('netbox_zabbix.jobs.sync_push.ZabbixAPI')
    def test_push_device_to_zabbix(self, mock_zabbix_api):
        """Test pushing device to Zabbix."""
        from netbox_zabbix.jobs.sync_push import PushSyncMixin

        # Mock the ZabbixAPI
        mock_instance = MagicMock()
        mock_zabbix_api.return_value = mock_instance
        mock_instance.host.update.return_value = [10001]

        # Create a mixin instance
        mixin = PushSyncMixin()
        mixin.logger = MagicMock()

        # Test push
        result = mixin.push_device_to_zabbix(self.device, self.zabbix_host)

        self.assertTrue(result)
        mock_instance.host.update.assert_called_once()

    @patch('netbox_zabbix.jobs.sync_push.ZabbixAPI')
    def test_push_device_to_zabbix_failure(self, mock_zabbix_api):
        """Test pushing device to Zabbix with failure."""
        from netbox_zabbix.jobs.sync_push import PushSyncMixin

        # Mock the ZabbixAPI to raise exception
        mock_zabbix_api.side_effect = Exception('Connection error')

        # Create a mixin instance
        mixin = PushSyncMixin()
        mixin.logger = MagicMock()

        # Test push
        result = mixin.push_device_to_zabbix(self.device, self.zabbix_host)

        self.assertFalse(result)

