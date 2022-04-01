"""
ASGI config for Symfall project.

It exposes the ASGI callable as a module-level variable named ``application``.

"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from messenger.websocket.handler import get_ws_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": get_ws_application(),
    }
)
