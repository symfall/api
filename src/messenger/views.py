from django.contrib.auth import logout
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser

from .permissions import IsAuthenticatedOrPostAllowAny
from .serializers import UserSerializer, ChatSerializer, MessageSerializer, MessageViewSerializer, \
    ChatViewSerializer, FileSerializer
from .models import Chat, Message, User, File


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrPostAllowAny,)


class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """
    queryset = Chat.objects.order_by('-updated_at')
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatViewSerializer
        else:
            return ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows message to be viewed or edited.
    """
    queryset = Message.objects.order_by('-created_at')
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MessageViewSerializer
        else:
            return MessageSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser,)
