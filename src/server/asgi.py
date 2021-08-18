"""
ASGI config for Symfall project.

It exposes the ASGI callable as a module-level variable named ``application``.

"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from messenger.middleware import TokenAuthMiddleware
from messenger.routers import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.default")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
        ),
    }
)
