import logging

from dcim.models import Device
from netbox import settings
from netbox_zabbix.utilities.helper import snmp_details

from netbox_zabbix.zabbix import Zabbix


__all__ = (
    'update_zabbix',
    'update_hostid'
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')

def update_hostid(zabbix, device, name=None):
    host = zabbix.host_get(host=name)
    if host and host.get('hostid', None):
        device.skip_signal = True
        device.custom_field_data['zabbix_hostid'] = int(host.get('hostid'))
        device.save()
    else:
        logger.info(f'Zabbix({device.name}): Host ID not set and unable to locate host in Zabbix')
        return


def update_zabbix(instance, hostid=None):

    status = 0
    if instance.status in ['offline', 'planned', 'inventory', 'staged', 'decommissioning']:
        status = 1

    if hasattr(instance, '_prechange_snapshot') and instance.name != instance._prechange_snapshot.get('name'):
        old_name = instance._prechange_snapshot.get('name')
    else:
        if isinstance(instance, Device) and instance.virtual_chassis and instance.virtual_chassis.name:
            old_name = instance.virtual_chassis.name
        else:
            old_name = instance.name
    try:
        zabbix = Zabbix()
        snmp = snmp_details(device=instance)
        hostid = instance.custom_field_data.get('zabbix_hostid', None)

        if not hostid:
            update_hostid(zabbix, instance, old_name)
        elif hostid and not zabbix.host_get(hostid=hostid):
            update_hostid(zabbix, instance, old_name)
            instance.refresh_from_db()
            hostid = instance.custom_field_data.get('zabbix_hostid', None)

        if isinstance(instance, Device):
            template = zabbix.template_get(instance.device_type.full_name)
        else:
            template = zabbix.template_get(instance.platform.name)

        if template is None:
            if isinstance(instance, Device):
                template = zabbix.template_get(
                    f'{instance.device_type.manufacturer.name} {instance.device_type.part_number}'
                )
            else:
                template = zabbix.template_get(
                    f'{instance.platform}'
                )


        group = instance.get_config_context().get('zabbix', {}).get('groups', [])
        group.extend(instance.get_config_context().get('zabbix', {}).get('tenants', []))
        group.extend(instance.get_config_context().get('zabbix', {}).get('locations', []))
        logger.info(f'Zabbix({instance.name}): Selected Groups')
        groups = []
        if isinstance(instance, Device) and instance.virtual_chassis and instance.virtual_chassis.name:
            name = instance.virtual_chassis.name
        else:
            name = instance.name
        for gid in group:
            groups.append({'groupid': f"{gid}"})
        if len(groups) == 0:
            groups.append({'groupid': f"{settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('group', None)}"})
        if template:
            logger.info(f'Zabbix({instance.name}): Starting update')
            result = zabbix.host_update(
                hostid=instance.custom_field_data.get('zabbix_hostid', None),
                name=name,
                ip=f'{instance.primary_ip.address.ip}',
                templates=[{'templateid': f"{template.get('templateid')}"}],
                groups=groups,
                snmp=snmp,
                status=status,
            )

            if not hostid:
                update_hostid(zabbix, instance, old_name)
            elif hostid and not zabbix.host_get(hostid=hostid):
                update_hostid(zabbix, instance, old_name)

            logger.info(result)
            logger.info(f'Zabbix({instance.name}): Complete for {instance.name}')
        else:
            logger.error(f'Zabbix({instance.name}): No template set ("{instance.device_type.full_name}") ')
    except Exception as e:
        import traceback
        logger.error(f'Zabbix({instance.name}): Exception: {e}')
        logger.error(traceback.format_exc())
