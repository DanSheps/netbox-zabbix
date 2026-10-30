import logging

from netbox import settings
from zabbix_utils import ZabbixAPI

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


class Zabbix:
    """Zabbix API wrapper using zabbix_utils.ZabbixAPI"""

    api = None
    url = None
    token = None

    def __init__(self):
        """Initialize Zabbix API from plugin configuration"""
        if not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('url', None):
            logger.error('Zabbix: No Zabbix URL configured')
            raise Exception('Zabbix URL not configured')
        elif not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('username', None):
            logger.error('Zabbix: No Zabbix username configured')
            raise Exception('Zabbix username not configured')
        elif not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('password', None):
            logger.error('Zabbix: No Zabbix password configured')
            raise Exception('Zabbix password not configured')

        self.url = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('url', None)
        username = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get(
            'username', None
        )
        password = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get(
            'password', None
        )

        try:
            # Use ZabbixAPI with username/password for backward compatibility
            # with settings-based configuration
            self.api = ZabbixAPI(
                url=self.url,
                user=username,
                password=password,
            )
        except Exception as e:
            logger.error(f'Failed to initialize Zabbix API: {e}')
            raise

    def template_get(self, name):
        """Get template by name"""
        try:
            results = self.api.template.get(filter={'host': name})  # type: ignore
            if len(results) > 1:
                raise Exception('Too many templates found')
            elif len(results) == 0:
                return None
            return results[0]
        except Exception as e:
            logger.error(f'Error getting template {name}: {e}')
            return None

    @staticmethod
    def build_interface(snmp, ip):
        """Build SNMP interface configuration"""
        if snmp:
            interfaces = []
            interface_type = 2
            main = 1
            port = '161'
            if snmp.get('version', None) in ('2', '2c', '3', '1'):
                data = {
                    'type': interface_type,
                    'main': main,
                    'useip': 1,
                    'ip': ip,
                    'dns': '',
                    'port': port,
                    'details': {},
                }
                for key, value in snmp.items():
                    data['details'][key] = value
                interfaces.append(data)

            logger.debug(f'Built interfaces: {interfaces}')
            if len(interfaces) > 0:
                return {'interfaces': interfaces}
            else:
                return {}
        else:
            return {}

    @staticmethod
    def build_macro(name, value):
        """Build macro configuration"""
        if name and value:
            logger.debug('Building Macros')
            return {'macros': [{'macro': '{$' + name + '}', 'value': f'{value}'}]}
        else:
            return {}

    def hostinterface_get(self, hostid):
        """Get host interface"""
        try:
            results = self.api.hostinterface.get(hostids=[hostid])  # type: ignore
            if len(results) > 1:
                raise Exception('Too many interfaces found')
            elif len(results) == 0:
                return None
            return results[0]
        except Exception as e:
            logger.error(f'Error getting host interface {hostid}: {e}')
            return None

    def hostinterface_update(self, hostid, interfaceid, ip=None, snmp=None):
        """Update host interface"""
        if snmp is None:
            snmp = {}
        try:
            data = {'interfaceid': interfaceid}
            if ip:
                data['ip'] = f'{ip}'
            for key, value in snmp.items():
                if 'details' not in data:
                    data['details'] = {}
                data['details'][key] = value

            result = self.api.hostinterface.update(**data)  # type: ignore
            return result
        except Exception as e:
            logger.error(f'Error updating host interface {interfaceid}: {e}')
            return None

    def host_get(self, host=None, hostid=None):
        """Get host by name or ID"""
        try:
            if hostid:
                results = self.api.host.get(hostids=[int(hostid)])  # type: ignore
            else:
                results = self.api.host.get(filter={'host': host})  # type: ignore

            if len(results) > 1:
                raise Exception('Too many hosts found')
            elif len(results) == 0:
                return None
            return results[0]
        except Exception as e:
            logger.error(f'Error getting host {host or hostid}: {e}')
            return None

    def host_create(
        self, name, ip, templates, groups, type=2, main=1, port=161, snmp=None, status=0
    ):
        """Create a new host"""
        if snmp is None:
            snmp = {}

        host = self.host_get(host=name)

        if not host:
            data = {
                'host': name,
                'groups': groups,
                'templates': templates,
                'inventory_mode': 1,
                'status': status,
            }
            if ip and snmp:
                logger.info(
                    f'Building Host Interface for {name} with IP {ip} and SNMP {snmp}'
                )
                data.update(self.build_interface(snmp=snmp, ip=ip))
                logger.debug(f'Host data: {data}')
            if snmp:
                community = snmp.get('community')
                data.update(self.build_macro('SNMP_COMMUNITY', community))

            try:
                result = self.api.host.create(**data)  # type: ignore
                return result
            except Exception as e:
                logger.error(f'Error creating host {name}: {e}')
                return None
        else:
            raise Exception('Cannot Create: Host Exists')

    def host_update(
        self,
        hostid,
        name,
        ip,
        templates,
        groups,
        type=2,
        main=1,
        port=161,
        snmp=None,
        status=0,
    ):
        """Update an existing host"""
        if snmp is None:
            snmp = {}

        host = None
        if hostid:
            host = self.host_get(hostid=hostid)
        else:
            host = self.host_get(host=name)

        if host:
            interface = self.hostinterface_get(hostid=hostid)
            data = {
                'hostid': f'{hostid}',
                'host': name,
                'templates': templates,
                'groups': groups,
                'status': status,
            }
            if snmp:
                data.update(
                    self.build_macro('SNMP_COMMUNITY', snmp.get('community', None))
                )

            try:
                result = self.api.host.update(**data)  # type: ignore
            except Exception as e:
                logger.error(f'Error updating host {hostid}: {e}')
                return None

            if interface:
                logger.info(
                    f'Current IP: {interface.get("ip", None)} | Desired IP: {ip}'
                )
                logger.info(
                    f'Current SNMP Version: {interface.get("details", {}).get("version", None)} | Desired SNMP Version: {snmp.get("version", 2)}'
                )
                if (
                    ip
                    and interface.get('ip', None) != ip
                    or interface.get('details', {}).get('version', None)
                    != snmp.get('version', 2)
                ):
                    logger.info(
                        f'Updating Host Interface {hostid} due to mismatch in IP or SNMP version'
                    )
                    result['interface'] = self.hostinterface_update(
                        hostid=hostid,
                        interfaceid=interface.get('interfaceid'),
                        ip=ip,
                        snmp=snmp,
                    )

            return result
        else:
            return self.host_create(
                name, ip, templates, groups, type, main, port, snmp, status
            )
