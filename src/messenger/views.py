from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from messenger.models import Chat, File, Message
from messenger.serializers import (
    ChatSerializer,
    ChatViewSerializer,
    FileSerializer,
    MessageSerializer,
    MessageViewSerializer,
)


class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """

    lookup_value_regex = r"\d+"
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    ordering = ("-created_at",)
    http_method_names = (
        "get",
        "post",
        "delete",
        "put",
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatViewSerializer
        return ChatSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Chat.objects.all_mine_and_invited(user=self.request.user)
        return Chat.objects.all_mine(user=self.request.user)


class SearchChatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering = ("-created_at",)
    http_method_names = ("get",)
    serializer_class = ChatViewSerializer

    def get_queryset(self):
        return Chat.objects.exclude_mine_and_invited(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows message to be viewed or edited.
    """

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ("chat",)
    ordering = ("-created_at",)
    http_method_names = (
        "get",
        "post",
        "delete",
        "put",
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MessageViewSerializer
        return MessageSerializer

    def get_queryset(self):
        return Message.objects.all_mine(user=self.request.user)


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """

    serializer_class = FileSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("message",)
    ordering = ("-created_at",)
    http_method_names = (
        "get",
        "post",
        "delete",
        "put",
    )

    def get_queryset(self):
        return File.objects.all_mine(user=self.request.user)
