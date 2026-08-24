import logging

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django_rq import get_queue

from extras.models import TaggedItem
from dcim.models import Device
from virtualization.models import VirtualMachine

from netbox_zabbix.utilities.helper import can_do_update


__all__ = (
    'update_device',
    'update_vm',
    'delete_device',
    'm2m_device'
)


logger = logging.getLogger('netbox.plugins.netbox_zabbix')


@receiver(post_save, sender=Device)
def update_device(instance, **kwargs):
    if hasattr(instance, 'skip_signal') and instance.skip_signal:
        logger.debug(f'NetBox Zabbix: Skipped device Signal for {instance.name}')
        return
    if can_do_update(instance):
        logger.debug(f'NetBox Zabbix: Hit Signal for {instance.name}')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.update_zabbix_device',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        # Device no longer matches tags/conditions — delete host from Zabbix if it was created
        logger.info(f'No update available for {instance}, scheduling delete')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.delete_zabbix_device',
            description=f'zabbix_delete-{instance.name}',
            hostid=instance.custom_field_data.get('zabbix_hostid', None),
            name=instance.name,
        )


@receiver(post_delete, sender=Device)
def delete_device(instance, **kwargs):
    """Delete host from Zabbix when device is deleted from NetBox."""
    hostid = instance.custom_field_data.get('zabbix_hostid', None)
    logger.debug(f'NetBox Zabbix: Delete Signal for {instance.name} (hostid={hostid})')
    queue = get_queue('high')
    job = queue.enqueue(
        'netbox_zabbix.jobs.delete_zabbix_device',
        description=f'zabbix_delete-{instance.name}',
        hostid=hostid,
        name=instance.name,
    )


@receiver(post_save, sender=VirtualMachine)
def update_vm(instance, **kwargs):
    if hasattr(instance, 'skip_signal') and instance.skip_signal:
        logger.debug('NetBox Zabbix: Skipped VM Signal')
        return
    if can_do_update(instance):
        logger.debug('NetBox Zabbix: Hit Signal')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.update_zabbix_vm',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        logger.info(f'No update available for {instance}, scheduling delete')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.delete_zabbix_vm',
            description=f'zabbix_delete-{instance.name}',
            hostid=instance.custom_field_data.get('zabbix_hostid', None),
            name=instance.name,
        )


@receiver(m2m_changed, sender=Device)
def m2m_device(instance, **kwargs):
    action = kwargs.get('action', None)
    # React to both tag add AND remove (including the monitored tag)
    if action not in ['post_add', 'post_remove']:
        return
    if hasattr(instance, 'skip_signal') and instance.skip_signal:
        return

    if can_do_update(instance):
        logger.debug(f'NetBox Zabbix: Hit M2M ({action}) - Device {instance.name}')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.update_zabbix_device',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        # Device no longer matches tags (monitored removed) — delete from Zabbix
        logger.debug(f'NetBox Zabbix: Device {instance.name} no longer matches tags, deleting')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.delete_zabbix_device',
            description=f'zabbix_delete-{instance.name}',
            hostid=instance.custom_field_data.get('zabbix_hostid', None),
            name=instance.name,
        )


@receiver(m2m_changed, sender=VirtualMachine)
def m2m_vm(instance, **kwargs):
    action = kwargs.get('action', None)
    if action not in ['post_add', 'post_remove']:
        return
    if hasattr(instance, 'skip_signal') and instance.skip_signal:
        return

    if can_do_update(instance):
        logger.debug(f'NetBox Zabbix: Hit M2M ({action}) - VM {instance.name}')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.update_zabbix_vm',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.delete_zabbix_vm',
            description=f'zabbix_delete-{instance.name}',
            hostid=instance.custom_field_data.get('zabbix_hostid', None),
            name=instance.name,
        )
