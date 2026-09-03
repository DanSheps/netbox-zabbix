from django.utils.translation import gettext as _

from netbox.forms import PrimaryModelForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
)
from utilities.forms.rendering import FieldSet

from netbox_zabbix.models import ZabbixHostGroup


__all__ = ('ZabbixTemplateForm',)


class ZabbixTemplateForm(PrimaryModelForm):

    comments = CommentField()

    fieldsets = (
        FieldSet(
            'name',
        ),
    )

    class Meta:
        model = ZabbixHostGroup
        fields = (
            'name',
            'description',
            'comments',
            'owner',
            'tags',
        )
