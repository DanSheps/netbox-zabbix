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
            return
        elif not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('username', None):
            logger.error(f'Zabbix: No Zabbix username configured')
            return
        elif not settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('password', None):
            logger.error(f'Zabbix: No Zabbix password configured')
            return
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
        # Always create an SNMP interface: use public if no community is set
        interfaces = []
        interface_type = 2
        main = 1
        port = '161'
        community = '{$SNMP_COMMUNITY}'
        if snmp:
            if snmp.get('version', None) == '2' or snmp.get('version', None) == '2c':
                community = '{$SNMP_COMMUNITY}'
            if snmp.get('community'):
                community = snmp['community']
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
                'community': community,
            }
        })
        return {'interfaces': interfaces}

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
        return result

    def host_get(self, host=None, hostid=None):
        params = {
            'output': ['host', 'hostid', 'proxy_hostid', 'status'],
            'selectInterfaces': ['interfaceid', 'ip'],
        }
        if hostid:
            params['hostids'] = [int(hostid)]
        else:
            params['filter'] = {'host': host}

        data = {'method': 'host.get', 'params': params}
        response = self.jsonrpc.send_api_request(data)
        result = response.json()

        if len(result.get('result', [])) > 1:
            raise Exception('Too many hosts found')
        elif len(result.get('result', [])) == 0:
            return None

        return result.get('result', []).pop()

    def proxyid_get(self, hostid=None):
        """Return the proxyid a host is bound to.

        Zabbix 7.0.26 host.get does not expose proxy_hostid in the output
        (returns None even for admin roles), but proxy.get with selectHosts
        does. Build a hostid -> proxyid map from all proxies to resolve the
        binding reliably. The map is cached per instance to avoid one
        proxy.get call per host during bulk syncs.
        """
        if not hasattr(self, '_proxy_host_map'):
            self._proxy_host_map = {}
            data = {
                'method': 'proxy.get',
                'params': {
                    'output': ['proxyid', 'name'],
                    'selectHosts': ['hostid', 'host'],
                },
            }
            response = self.jsonrpc.send_api_request(data)
            for proxy in response.json().get('result', []):
                for host in proxy.get('hosts', []):
                    self._proxy_host_map[host['hostid']] = proxy['proxyid']
        if hostid:
            return self._proxy_host_map.get(str(hostid))
        return None

    def host_create(self, name, ip, templates, groups, type=2, main=1, port=161, snmp={}, status=0, inventory=None):
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
            if inventory:
                data['params']['inventory'] = inventory
            # Assign proxy on create if configured (avoids hosts landing on the server).
            # Zabbix 7.0 uses monitored_by + proxyid (proxy_hostid was removed).
            cfg_proxy = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('proxy', None)
            if cfg_proxy:
                data['params']['monitored_by'] = 1
                data['params']['proxyid'] = cfg_proxy
            if ip:
                data['params'].update(self.build_interface(snmp=snmp, ip=ip))
            # SNMP community: from config context or default public
            community = snmp.get('community') if snmp else 'public'
            data['params'].update(self.build_macro('SNMP_COMMUNITY', community))

            response = self.jsonrpc.send_api_request(data)
            result = response.json()
            return result
        else:
            raise Exception('Cannot Create: Host Exists')

    def host_update(self, hostid, name, ip, templates, groups, type=2, main=1, port=161, snmp={}, status=0, inventory=None):
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
            if inventory:
                # Zabbix 7.0 API ignores name/model/serialno_a/location on host.update;
                # only inventory_mode=1 hosts accept the rest. Pass what is writable.
                data['params']['inventory'] = inventory
            # Preserve proxy binding. In Zabbix 7.0 the parameter is
            # monitored_by=1 + proxyid (proxy_hostid no longer exists, and
            # host.get does not expose it). Resolve the real proxyid via
            # proxy.get selectHosts.
            cfg_proxy = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('proxy', None)
            if cfg_proxy:
                proxy_id = cfg_proxy
            else:
                proxy_id = self.proxyid_get(hostid=hostid)
            if proxy_id:
                data['params']['monitored_by'] = 1
                data['params']['proxyid'] = proxy_id
            if snmp:
                data['params'].update(self.build_macro('SNMP_COMMUNITY', snmp.get('community', None)))
            response = self.jsonrpc.send_api_request(data)
            result = response.json()

            if ip and interface.get('ip', None) != ip:
                # Only update interface if IP doesn't match
                result['interface'] = self.hostinterface_update(hostid=hostid, interfaceid=interface.get('interfaceid'), ip=ip)

            return result
        else:
            return self.host_create(name, ip, templates, groups, type, main, port, snmp, inventory)

    def host_delete(self, hostid=None, name=None):
        """Delete host from Zabbix (by hostid or by name)."""
        host = None
        if hostid:
            host = self.host_get(hostid=hostid)
        elif name:
            host = self.host_get(host=name)
        else:
            logger.error('host_delete: neither hostid nor name provided')
            return {'error': 'no hostid/name'}

        if not host:
            logger.info(f'host_delete: host not found (hostid={hostid}, name={name})')
            return {'result': 'not found'}

        data = {
            'method': 'host.delete',
            'params': [host['hostid']],
        }
        response = self.jsonrpc.send_api_request(data)
        result = response.json()
        logger.info(f'host_delete: {result}')
        return result
