import uuid
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django_prometheus.models import model_inserts, model_updates

from core.choices import ObjectChangeActionChoices, JobStatusChoices
from core.events import *
from extras.events import enqueue_event
from extras.models import Tag
from netbox.context import current_request, events_queue

from core.models import ConfigRevision, DataSource, ObjectChange, Job
from netbox_zabbix.models import *
from utilities.request import NetBoxFakeRequest


@receiver((post_save, m2m_changed))
def handle_changed_object_special(sender, instance, **kwargs):
    """
    Fires when an object is created or updated.
    """
    m2m_changed = False

    if not hasattr(instance, 'to_objectchange'):
        return

    # Get the current request, or bail if not set
    request = current_request.get()
    if request is not None:
        return

    if sender not in [
        ZabbixServer,
        ZabbixProxy,
        ZabbixProxyGroup,
        ZabbixHostGroup,
        ZabbixTemplate,
        ZabbixHost,
        ZabbixHostInterface,
        ZabbixHostInterfaceSNMP,
    ]:
        return

    # Determine the type of change being made
    if kwargs.get('created'):
        event_type = OBJECT_CREATED
    elif 'created' in kwargs:
        event_type = OBJECT_UPDATED
    elif kwargs.get('action') in ['post_add', 'post_remove'] and kwargs['pk_set']:
        # m2m_changed with objects added or removed
        m2m_changed = True
        event_type = OBJECT_UPDATED
    elif kwargs.get('action') == 'post_clear':
        # Handle clearing of an M2M field
        if kwargs.get('model') == Tag and getattr(
            instance, '_prechange_snapshot', {}
        ).get('tags'):
            # Handle generation of M2M changes for Tags which have a previous value (ignoring changes where the
            # prechange snapshot is empty)
            m2m_changed = True
            event_type = OBJECT_UPDATED
        else:
            # Other endpoints are unimpacted as they send post_add and post_remove
            # This will impact changes that utilize clear() however so we may want to give consideration for this branch
            return
    else:
        return

    job = Job.objects.filter(status=JobStatusChoices.STATUS_RUNNING).last()
    if job:
        request = NetBoxFakeRequest(
            {
                'id': Job.objects.filter(status=JobStatusChoices.STATUS_RUNNING)
                .last()
                .job_id,
            }
        )
    else:
        request = NetBoxFakeRequest(
            {
                'id': uuid.uuid4(),
            }
        )

    # Create/update an ObjectChange record for this change
    action = {
        OBJECT_CREATED: ObjectChangeActionChoices.ACTION_CREATE,
        OBJECT_UPDATED: ObjectChangeActionChoices.ACTION_UPDATE,
        OBJECT_DELETED: ObjectChangeActionChoices.ACTION_DELETE,
    }[event_type]
    objectchange = instance.to_objectchange(action)
    # If this is a many-to-many field change, check for a previous ObjectChange instance recorded
    # for this object by this request and update it
    if m2m_changed and (
        prev_change := ObjectChange.objects.filter(
            changed_object_type=ContentType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
            request_id=request.id,
        ).first()
    ):
        prev_change.postchange_data = objectchange.postchange_data
        prev_change.save()
    elif objectchange and objectchange.has_changes:
        objectchange.user_name = 'System Job'
        objectchange.request_id = request.id
        objectchange.save()

    # Ensure that we're working with fresh M2M assignments
    if m2m_changed:
        instance.refresh_from_db()

    # Increment metric counters
    if event_type == OBJECT_CREATED:
        model_inserts.labels(instance._meta.model_name).inc()
    elif event_type == OBJECT_UPDATED:
        model_updates.labels(instance._meta.model_name).inc()
