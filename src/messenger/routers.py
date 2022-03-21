from django.urls import re_path
from rest_framework.routers import DefaultRouter

from messenger.views import (
    ChatViewSet,
    FileViewSet,
    MessageViewSet,
    SearchChatViewSet,
)
from messenger.websocket.consumers import ChatConsumer

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
        name="chat-poll",
    ),
]
