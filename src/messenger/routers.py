from django.urls import re_path
from rest_framework.routers import DefaultRouter

from messenger.consumers import ChatConsumer
from messenger.views import (
    ChatViewSet,
    FileViewSet,
    MessageViewSet,
    SearchChatViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(
    prefix="chat",
    viewset=ChatViewSet,
    basename="chat",
)
router.register(
    prefix="chat/search",
    viewset=SearchChatViewSet,
    basename="chat_search",
)
router.register(
    prefix="message",
    viewset=MessageViewSet,
    basename="message",
)
router.register(
    prefix="file",
    viewset=FileViewSet,
    basename="file",
)

websocket_urlpatterns = [
    re_path(
        route=r"ws/chat/(?P<chat_id>\d+)$",
        view=ChatConsumer.as_asgi(),
    ),
]
