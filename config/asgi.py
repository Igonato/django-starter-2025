"""
ASGI config for the project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from . import routing  # noqa

application = ProtocolTypeRouter(
    {
        # Regular Django views
        "http": django_asgi_app,
        # WebSocket consumers
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.urlpatterns))
        ),
        # Background workers
        "channel": ChannelNameRouter(routing.name_routes),
    }
)
