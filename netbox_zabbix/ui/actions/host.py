import logging

from django.utils.translation import gettext as _

from typing import Any

from django.apps import apps
from django.utils.translation import gettext_lazy as _

from netbox.ui.actions import LinkAction, PanelAction
from netbox_zabbix.models import ZabbixHostInterface
from utilities.permissions import get_permission_for_model
from utilities.views import get_viewname

logger = logging.getLogger('netbox.plugins.netbox_zabbix.ui.actions.hosts')


class AddOrEditInterface(PanelAction):
    """Render an add or edit link for the parent interface's SNMP settings."""

    def __init__(
        self,
        parent: Any,
        model: str = 'netbox_zabbix.ZabbixHostInterfaceSNMP',
        **kwargs: Any,
    ) -> None:
        super().__init__(label=kwargs.get('label', _('Add')))
        logger.debug(kwargs)
        self.parent = parent
        self.action_kwargs = dict(kwargs)

        try:
            self.model = apps.get_model(model)
        except LookupError as exc:
            raise ValueError(f'Unable to find interface model: {model}') from exc

    def render(self, context: dict[str, Any]) -> str:
        parent = self.parent(context) if callable(self.parent) else self.parent

        if not parent:
            logger.debug('No parent interface provided for AddOrEditInterface action.')
            raise ValueError(
                'No parent interface provided for AddOrEditInterface action.'
            )
        try:
            interface = self.model.objects.get(interface_id=parent.pk)
        except self.model.DoesNotExist:
            interface = None
            mode = 'add'
            view_kwargs = {}
            url_params = {'interface': parent.pk}
        else:
            mode = 'edit'
            view_kwargs = {'pk': interface.pk}
            url_params = {}

        kwargs = self.action_kwargs.copy()
        kwargs.setdefault('label', _('Edit') if mode == 'edit' else _('Add'))
        kwargs.setdefault('button_icon', 'pencil' if mode == 'edit' else 'plus-thick')
        kwargs.setdefault(
            'permissions',
            [
                get_permission_for_model(
                    self.model, 'change' if mode == 'edit' else 'add'
                )
            ],
        )

        return LinkAction(
            view_name=get_viewname(self.model, mode),
            view_kwargs=view_kwargs,
            url_params={
                'return_url': parent.get_absolute_url(),
                **url_params,
            },
            **kwargs,
        ).render(context)
