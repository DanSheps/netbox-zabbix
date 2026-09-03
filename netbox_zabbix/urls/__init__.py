from django.urls import include, path
from django.apps import apps
from utilities.urls import get_model_urls

from netbox_zabbix import views

__all__ = ('urlpatterns',)


app_name = 'netbox_zabbix'
patterns = []
for models in apps.get_app_config(app_name).get_models():
    url_name = models._meta.verbose_name.lower().replace(' ', '-')
    model_name = models._meta.model_name
    patterns.append(
        path(
            f'{url_name}/', include(get_model_urls(app_name, model_name, detail=False))
        )
    )
    patterns.append(
        path(f'{url_name}/<int:pk>/', include(get_model_urls(app_name, model_name)))
    )

urlpatterns = patterns
