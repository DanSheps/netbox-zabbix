import logging

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django_rq import get_queue

from extras.models import TaggedItem
from dcim.models import Device
from virtualization.models import VirtualMachine

from netbox_zabbix.utilities.helper import can_do_update


__all__ = (
    'update_device',
    'update_vm',
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
        logger.info(f'No update available for {instance}')


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
        logger.info(f'No update available for {instance}')


@receiver(m2m_changed, sender=VirtualMachine)
def m2m_device(instance, **kwargs):
    if (
            kwargs.get('action', None) not in ['post_add'] or
            not kwargs.get('pk_set') or
            (
                not isinstance(instance, Device) and not isinstance(instance, VirtualMachine)
            )
            or
            (
                hasattr(instance, 'skip_signal') and instance.skip_signal
            )
    ):
        return
    if can_do_update(instance) and isinstance(instance, Device):
        logger.debug('NetBox Zabbix: Hit M2M - Device')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.update_zabbix_device',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    elif can_do_update(instance) and isinstance(instance, VirtualMachine):
        logger.debug('NetBox Zabbix: Hit M2M - VirtualMachine')
        queue = get_queue('high')
        job = queue.enqueue(
            'netbox_zabbix.jobs.update_zabbix_vm',
            description=f'zabbix_update-{instance.name}',
            pk=instance.pk,
        )
    else:
        logger.info(f'No update available for {instance}')
