
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Test the Zabbix API"

    def handle(self, *args, **kwargs):
        from netbox_zabbix.zabbix import Zabbix
        try:
            zabbix = Zabbix()
        except Exception as e:
            print(e)