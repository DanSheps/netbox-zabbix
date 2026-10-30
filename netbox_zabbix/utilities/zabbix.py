import logging

from dcim.models import Device, VirtualDeviceContext
from netbox import settings
from zabbix_utils import ZabbixAPI
from netbox_zabbix.utilities.helper import snmp_details


__all__ = (
    'update_zabbix',
    'update_hostid'
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')


def _get_zabbix_api():
    """Get ZabbixAPI instance from plugin configuration"""
    url = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('url', None)
    username = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('username', None)
    password = settings.PLUGINS_CONFIG.get('netbox_zabbix', {}).get('password', None)

    if not url or not username or not password:
        raise Exception('Zabbix configuration not found in settings')

    return ZabbixAPI(
        url=url,
        user=username,
        password=password,
    )


def update_hostid(zabbix_api, device, name=None):
    """Update device custom field with Zabbix host ID"""
    try:
        hosts = zabbix_api.host.get(filter={'host': name})  # type: ignore
        if hosts and hosts[0].get('hostid', None):
            device.skip_signal = True
            device.custom_field_data['zabbix_hostid'] = int(hosts[0].get('hostid'))
            device.save()
        else:
            logger.info(f'Zabbix({device.name}): Host ID not set and unable to locate host in Zabbix')
    except Exception as e:
        logger.error(f'Error updating host ID for {device.name}: {e}')


def update_zabbix(instance, hostid=None):
    """Update device/VM in Zabbix"""

    device = instance
    if isinstance(instance, VirtualDeviceContext):
        device = instance.device

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
        zabbix = _get_zabbix_api()
        snmp = snmp_details(instance=instance)
        hostid = instance.custom_field_data.get('zabbix_hostid', None)

        if not hostid:
            update_hostid(zabbix, instance, old_name)
        else:
            # Verify host still exists
            try:
                hosts = zabbix.host.get(hostids=[hostid])  # type: ignore
                if not hosts:
                    update_hostid(zabbix, instance, old_name)
                    instance.refresh_from_db()
                    hostid = instance.custom_field_data.get('zabbix_hostid', None)
            except Exception:
                update_hostid(zabbix, instance, old_name)
                instance.refresh_from_db()
                hostid = instance.custom_field_data.get('zabbix_hostid', None)

        if isinstance(instance, Device):
            templates = zabbix.template.get(filter={'host': instance.device_type.full_name})  # type: ignore
            template = templates[0] if templates else None
        elif isinstance(instance, VirtualDeviceContext):
            templates = zabbix.template.get(filter={'host': instance.device.device_type.full_name})  # type: ignore
            template = templates[0] if templates else None
        else:
            templates = zabbix.template.get(filter={'host': instance.platform.name})  # type: ignore
            template = templates[0] if templates else None

        if template is None:
            if isinstance(instance, Device):
                templates = zabbix.template.get(  # type: ignore
                    filter={'host': f'{instance.device_type.manufacturer.name} {instance.device_type.part_number}'}
                )
                template = templates[0] if templates else None
            else:
                templates = zabbix.template.get(filter={'host': f'{instance.platform}'})  # type: ignore
                template = templates[0] if templates else None

        group = device.get_config_context().get('zabbix', {}).get('groups', [])
        group.extend(device.get_config_context().get('zabbix', {}).get('tenants', []))
        group.extend(device.get_config_context().get('zabbix', {}).get('locations', []))
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
            result = zabbix.host.update(  # type: ignore
                hostid=hostid,
                name=name,
                groups=groups,
            )

            # Update interface with IP if available
            if instance.primary_ip:
                try:
                    interfaces = zabbix.hostinterface.get(hostids=[hostid])  # type: ignore
                    if interfaces:
                        zabbix.hostinterface.update(  # type: ignore
                            interfaceid=interfaces[0].get('interfaceid'),
                            ip=str(instance.primary_ip.address.ip),
                        )
                        # Update SNMP details if needed
                        if snmp:
                            details = {}
                            for key, value in snmp.items():
                                details[key] = value
                            if details:
                                zabbix.hostinterface.update(  # type: ignore
                                    interfaceid=interfaces[0].get('interfaceid'),
                                    details=details,
                                )
                except Exception as e:
                    logger.warning(f'Could not update interface for {instance.name}: {e}')

            # Update templates if different
            if template:
                try:
                    zabbix.host.update(  # type: ignore
                        hostid=hostid,
                        templates=[{'templateid': f"{template.get('templateid')}"}],
                    )
                except Exception as e:
                    logger.warning(f'Could not update templates for {instance.name}: {e}')

            if not hostid:
                update_hostid(zabbix, instance, old_name)
            elif hostid:
                # Verify host still has ID after update
                try:
                    hosts = zabbix.host.get(hostids=[hostid])  # type: ignore
                    if not hosts:
                        update_hostid(zabbix, instance, old_name)
                except Exception:
                    update_hostid(zabbix, instance, old_name)

            logger.info(result)
            logger.info(f'Zabbix({instance.name}): Complete for {instance.name}')
        else:
            logger.error(f'Zabbix({instance.name}): No template set ("{instance.device_type.full_name}") ')
    except Exception as e:
        import traceback
        logger.error(f'Zabbix({instance.name}): Exception: {e}')
        logger.error(traceback.format_exc())
