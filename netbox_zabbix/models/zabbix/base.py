from django.db import models
from django.utils.translation import gettext as _


class ZabbixID(models.Model):
    zid = models.PositiveIntegerField(
        verbose_name=_('Zabbix Object ID'),
        help_text=_('The unique identifier for this object in Zabbix.'),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def instantiate(cls, server, entry, key_field):
        return cls(
            zid=entry.get(key_field),
            server=server,
        )

    @classmethod
    def get_additional_filter_query_params(cls, server, entry):
        return {'server': server}

    @classmethod
    def get_model_name(cls):
        return cls._meta.model_name.replace('zabbix', '')

    @classmethod
    def get_zid_field_name(cls):
        return f'{cls.get_model_name()}id'

    @classmethod
    def get_name_field_name(cls):
        return 'name'

    @classmethod
    def get_query_flags(cls):
        return {}

    @classmethod
    def get_api_name(cls):
        return f'{cls.get_model_name()}'
