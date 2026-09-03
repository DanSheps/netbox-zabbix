from django.db.models import Q

__all__ = ('ZABBIX_ASSIGNMENT_MODELS',)


ZABBIX_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='device')
    | Q(app_label='dcim', model='virtualdevicecontext')
    | Q(app_label='dcim', model='virtualchassis')
    | Q(app_label='virtualization', model='clustergroup')
    | Q(app_label='virtualization', model='cluster')
    | Q(app_label='virtualization', model='virtualmachine')
)
