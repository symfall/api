from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.parsers import MultiPartParser

from messenger.models import Chat, File, Message
from messenger.permissions import IsAuthenticatedOrPostAllowAny
from messenger.serializers import (
    ChatSerializer,
    ChatViewSerializer,
    FileSerializer,
    MessageSerializer,
    MessageViewSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    http_method_names = ("get", "put", "delete", "patch")
    queryset = get_user_model().objects.order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrPostAllowAny,)


class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """

    queryset = Chat.objects.order_by("-updated_at")
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatViewSerializer
        return ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows message to be viewed or edited.
    """

    queryset = Message.objects.order_by("-created_at")
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MessageViewSerializer
        return MessageSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser,)
