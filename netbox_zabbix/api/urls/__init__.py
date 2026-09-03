from netbox.api.routers import NetBoxRouter
from netbox_zabbix.api.views import *

router = NetBoxRouter()
router.register('server', ZabbixServerViewSet)
router.register('proxy-group', ZabbixProxyGroupViewSet)
router.register('proxy', ZabbixProxyViewSet)
router.register('host-group', ZabbixHostGroupViewSet)
router.register('host', ZabbixHostViewSet)
router.register('template', ZabbixTemplateViewSet)
router.register('host-interface', ZabbixHostInterfaceViewSet)
router.register('host-interface-snmp', ZabbixHostInterfaceSNMPViewSet)
urlpatterns = router.urls
