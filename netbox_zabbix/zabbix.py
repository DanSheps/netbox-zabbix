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
            if snmp.get('version', None) == '2' or snmp.get('version', None) == '2c':
                interfaces.append({
                    'type': interface_type,
                    'main': main,
                    'useip': 1,
                    'ip': ip,
                    'dns': '',
                    'port': port,
                        'details': {
                        'version': 2,
                        'bulk': 0,
                        'community': '{$SNMP_COMMUNITY}'
                    }
                })

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

    def hostinterface_update(self, hostid, interfaceid, ip=None):
        data = {
            'method': 'hostinterface.update',
            'params': {
                'interfaceid': interfaceid
            },
        }
        if ip:
            data['params'].update({'ip': f'{ip}'})
        response = self.jsonrpc.send_api_request(data)
        result = response.json()

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
                data['params'].update(self.build_interface(snmp=snmp, ip=ip))
            if snmp:
                community = snmp.get('community')
                data['params'].update(self.build_macro('SNMP_COMMUNITY', community))

            response = self.jsonrpc.send_api_request(data)
            result = response.json()
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

            if ip and interface.get('ip', None) != ip:
                # Only update interface if IP doesn't match
                self.hostinterface_update(hostid=hostid, interfaceid=interface.get('interfaceid'), ip=ip)
        else:
            self.host_create(name, ip, templates, groups, type, main, port, snmp)
