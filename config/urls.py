"""
URL configuration for the project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from importlib.util import find_spec

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.debug import default_urlconf

urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
]

if settings.USE_HEALTH_CHECK and settings.HEALTH_CHECK_PATH:
    urlpatterns += [
        path(settings.HEALTH_CHECK_PATH, include("health_check.urls")),
    ]

if settings.DEBUG:
    urlpatterns += [
        # Restore the default view that displays Django welcome page
        # (normally it would be gone when we include extra urls like the
        # ones from the Debug Toolbar or django-browser-reload)
        path("", default_urlconf),
    ]

# Automatically add urlpatterns from urls.py for installed project apps
for app in apps.get_app_configs():
    if not app.path.startswith(str(settings.BASE_DIR)):
        continue
    if app.path.startswith(str(settings.BASE_DIR / ".venv")):
        continue

    module = app.name + ".urls"
    if find_spec(module) is not None and module != __name__:
        urlpatterns += [path("", include(module))]

if (
    settings.DEBUG
    and find_spec("debug_toolbar") is not None
    and find_spec("django_browser_reload") is not None
):
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        # Debug toolbar URLs
        path("__debug__/", include(debug_toolbar.urls)),
        # Development auto-reload endpoint
        path("__reload__/", include("django_browser_reload.urls")),
        # Serve uploaded files during development
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
