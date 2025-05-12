from importlib import import_module
from importlib.util import find_spec

from django.apps import apps
from django.conf import settings

urlpatterns = []
name_routes = {}


# Automatically add urlpatterns from routing.py for installed project apps
for app in apps.get_app_configs():
    if not app.path.startswith(str(settings.BASE_DIR)):
        continue
    if app.path.startswith(str(settings.BASE_DIR / ".venv")):
        continue

    module = app.name + ".routing"
    if find_spec(module) is not None and module != __name__:
        routing = import_module(module)
        urlpatterns += getattr(routing, "urlpatterns", [])
        urlpatterns += getattr(routing, "websocket_urlpatterns", [])
        name_routes.update(getattr(routing, "name_routes", {}))
