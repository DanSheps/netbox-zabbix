import logging

from netbox import settings
from netbox_zabbix.jsonrpc import JSONRPC

logger = logging.getLogger('netbox.plugins.netbox_zabbix')


class Zabbix:
    jsonrpc = None

    url = None
    username = None
    password = None

    def __init__(self):

        if not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('url', None):
            logger.error(f'Zabbix: No Zabbix URL configured')
            return False
        elif not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('username', None):
            logger.error(f'Zabbix: No Zabbix username configured')
            return False
        elif not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('password', None):
            logger.error(f'Zabbix: No Zabbix password configured')
            return False
        else:
            self.url = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('url', None)
            self.username =  settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('username', None)
            self.password = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('password', None)

        self.jsonrpc = JSONRPC(url=self.url, username=self.username, password=self.password)

    def template_get(self, name):
        data = {
            'method': 'template.get',
            'params': {
                "output": [
                    "hostid"
                ],
                "filter": {
                    "host": name
                }
            },
        }

        response = self.jsonrpc.send_api_request(data)
        result = response.json()

        if len(result.get('result', [])) > 1:
            raise Exception('Too many hosts found')
        elif len(result.get('result', [])) == 0:
            return None

        return result.get('result', []).pop()

    @staticmethod
    def build_interface(snmp, ip):
        if snmp:
            interfaces = []
            interface_type = 2
            main = 1
            port = '161'
            if snmp.get('version', None) == '2' or snmp.get('version', None) == '2c' or snmp.get('version', None) == '3':
                data = {
                    'type': interface_type,
                    'main': main,
                    'useip': 1,
                    'ip': ip,
                    'dns': '',
                    'port': port,
                        'details': {
                    }
                }
                for key, value in  snmp.items():
                    data['details'][key] = value
                interfaces.append(data)
            logger.debug(f'\t\t{interfaces}')
            if len(interfaces) > 0:
                return {'interfaces': interfaces}
            else:
                return {}
        else:
            return {}

    @staticmethod
    def build_macro(name, value):
        if name and value:
            logger.debug(f'\tZabbix: Building Macros')
            return {'macros': [
                        {
                            'macro': '{$' + name + '}',
                            'value': f'{value}'
                        }
                    ]}
        else:
            return {}

    def hostinterface_get(self, hostid):
        data = {
            'method': 'hostinterface.get',
            'params': {
                'hostids': [hostid]
            },
        }

        response = self.jsonrpc.send_api_request(data)
        result = response.json()

        if len(result.get('result', [])) > 1:
            raise Exception('Too many hosts found')
        elif len(result.get('result', [])) == 0:
            return None

        return result.get('result', []).pop()

    def hostinterface_update(self, hostid, interfaceid, ip=None, snmp={}):
        data = {
            'method': 'hostinterface.update',
            'params': {
                'interfaceid': interfaceid
            },
        }
        if ip:
            data['params'].update({'ip': f'{ip}'})
        for key, value in snmp.items():
            if data['params'].get('details') is None:
                data['params']['details'] = {}
            data['params']['details'][key] = value
        response = self.jsonrpc.send_api_request(data)
        result = response.json()
        return result

    def host_get(self, host=None, hostid=None):
        if hostid:
            data = {
                'method': 'host.get',
                'params': {
                    'hostids': [int(hostid)]
                },
            }
        else:
            data = {
                'method': 'host.get',
                'params': {
                    "filter": {
                        "host": host
                    }
                },
            }

        response = self.jsonrpc.send_api_request(data)
        result = response.json()

        if len(result.get('result', [])) > 1:
            raise Exception('Too many hosts found')
        elif len(result.get('result', [])) == 0:
            return None

        return result.get('result', []).pop()

    def host_create(self, name, ip, templates, groups, type=2, main=1, port=161, snmp={}, status=0):
        host = self.host_get(host=name)

        if not host:
            data = {
                'method': 'host.create',
                'params': {
                    'host': name,
                    'groups': groups,
                    'templates': templates,
                    "inventory_mode": 1,
                    "status": status,
                },
            }
            if ip and snmp:
                logger.info(f'\tZabbix: Building Host Interface for {name} with IP {ip} and SNMP {snmp}')
                data['params'].update(self.build_interface(snmp=snmp, ip=ip))
                logger.debug(f'\tZabbix: {data["params"]}')
            if snmp:
                community = snmp.get('community')
                data['params'].update(self.build_macro('SNMP_COMMUNITY', community))

            response = self.jsonrpc.send_api_request(data)
            result = response.json()
            return result
        else:
            raise Exception('Cannot Create: Host Exists')

    def host_update(self, hostid, name, ip, templates, groups, type=2, main=1, port=161, snmp={}, status=0):
        host = None
        if hostid:
            host = self.host_get(hostid=hostid)
        else:
            host = self.host_get(host=name)

        if host:
            interface = self.hostinterface_get(hostid=hostid)
            data = {
                'method': 'host.update',
                'params': {
                    'hostid': f'{hostid}',
                    'host': name,
                    'templates': templates,
                    'groups': groups,
                    'status': status,
                },
            }
            if snmp:
                data['params'].update(self.build_macro('SNMP_COMMUNITY', snmp.get('community', None)))
            response = self.jsonrpc.send_api_request(data)
            result = response.json()

            logger.info(
                f'\t\tZabbix: Current IP: {interface.get("ip", None)} | Desired IP: {ip}'
            )
            logger.info(
                f'\t\tZabbix: Current SNMP Version: {interface.get("details", {}).get("version", None)} | Desired SNMP Version: {snmp.get("version", 2)}'
            )
            if ip and interface.get('ip', None) != ip or interface.get('details', {}).get('version', None) != snmp.get('version', 2):
                # Only update interface if IP doesn't match
                logger.info(f'\tZabbix: Updating Host Interface {hostid} due to mismatch in IP or SNMP version')
                result['interface'] = self.hostinterface_update(hostid=hostid, interfaceid=interface.get('interfaceid'), ip=ip, snmp=snmp)

            return result
        else:
            return self.host_create(name, ip, templates, groups, type, main, port, snmp)
