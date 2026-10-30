
from django.core.management.base import BaseCommand
from netbox import settings
from zabbix_utils import ZabbixAPI


class Command(BaseCommand):
    help = "Test the Zabbix API"

    def handle(self, *args, **kwargs):
        try:
            url = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('url', None)
            username = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('username', None)
            password = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('password', None)

            if not url or not username or not password:
                print('Zabbix configuration not found in settings')
                return

            zabbix = ZabbixAPI(
                url=url,
                user=username,
                password=password,
            )
            print(f'Successfully connected to Zabbix API at {url}')
        except Exception as e:
            print(f'Error connecting to Zabbix API: {e}')

