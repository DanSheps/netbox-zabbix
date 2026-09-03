from django.utils.translation import gettext as _
from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox_zabbix.models import *

app_name = 'netbox_zabbix'

navs = (
    ('Zabbix', (ZabbixServer, ZabbixProxyGroup, ZabbixProxy)),
    (
        'Templates',
        (
            ZabbixTemplate,
            ZabbixHostTemplate,
        ),
    ),
    (
        'Hosts',
        (
            ZabbixHostGroup,
            ZabbixHost,
            ZabbixHostInterface,
        ),
    ),
)

patterns = []

menus = []
for nav, models in navs:
    menu_group = []
    for model in models:
        url_name = model._meta.verbose_name.lower().replace(' ', '-')
        model_name = model._meta.model_name
        menu_group.append(
            PluginMenuItem(
                link=f'plugins:{app_name}:{model_name}_list',
                link_text=_(f'{model._meta.verbose_name_plural}'),
                permissions=[f'{app_name}.view_{model_name}'],
                buttons=(
                    PluginMenuButton(
                        link=f'plugins:{app_name}:{model_name}_add',
                        title=_('Add'),
                        icon_class='mdi mdi-plus',
                        permissions=[f'{app_name}.add_{model_name}'],
                    ),
                    # PluginMenuButton(f'plugins:{app_name}:{model_name}_bulk_import', 'Import', 'mdi mdi-upload'),
                ),
            )
        )
    menus.append((f'{nav}', tuple(menu_group)))
    # url_name = models._meta.verbose_name.lower().replace(' ', '-')
    # model_name = models._meta.model_name

menu = PluginMenu(
    label='Netbox Zabbix',
    groups=tuple(menus),
    icon_class='mdi mdi-server-network',
)
