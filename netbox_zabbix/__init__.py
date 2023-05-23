from extras.plugins import PluginConfig
from importlib.metadata import metadata

metadata = metadata('netbox_zabbix')

class ZabbixPlugin(PluginConfig):
    name = metadata.get('Name').replace('-', '_')
    verbose_name = metadata.get('Summary')
    description = metadata.get('Description')
    version = metadata.get('Version')
    author = metadata.get('Author')
    author_email = metadata.get('Author-email')
    base_url = 'zabbix'
    min_version = '3.2.0'
    max_version = '3.5.99'
    required_settings = [
        'username',
        'password',
    ]
    default_settings = {
        'tags': ['automation: monitoring'],
        'snmp': {
            'version': '2c',  # 1, 2c, 3
            'community': None,
            'context': None,
            'username': None,
            'level': None,  # None, noAuthNoPriv, authNoPriv, authPriv
            'auth_protocol': None,  # None, MD5, SHA1, SHA224, SHA256, SHA384, SHA512
            'auth_passphrase': None,
            'priv_protocol': None,  # None, DES, AES128, AES192, AES256, AES192C, AES256C
            'priv_passphrase': None,
        }
    }
    queues = []

    def ready(self):
        super().ready()
        import netbox_zabbix.signals


config = ZabbixPlugin
