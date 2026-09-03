from netbox.ui.attrs import ObjectAttribute


class HyperLinkAttr(ObjectAttribute):
    """
    A text attribute.

    Parameters:
         style (str): CSS class to apply to the rendered attribute
         format_string (str): If specified, the value will be formatted using this string when rendering
         copy_button (bool): Set to True to include a copy-to-clipboard button
    """

    template_name = 'netbox_zabbix/ui/attrs/hyperlink.html'

    def __init__(self, *args, style=None, copy_button=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = style
        self.copy_button = copy_button

    def get_context(self, obj, attr, value, context):
        return {
            'copy_button': self.copy_button,
        }
