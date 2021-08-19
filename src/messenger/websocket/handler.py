from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from messenger.routers import websocket_urlpatterns
from messenger.websocket.middleware import TokenAuthMiddleware


def get_ws_application():
    application = URLRouter(websocket_urlpatterns)
    application = TokenAuthMiddleware(application)
    application = AllowedHostsOriginValidator(application)

    return application
