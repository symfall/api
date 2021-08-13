from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser

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
    permission_classes = (permissions.IsAuthenticated,)
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
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 30

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatViewSerializer
        return ChatSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Chat.objects.filter(
                Q(creator=self.request.user.id)
                | Q(invited=self.request.user.id)
            )
        return Chat.objects.filter(Q(creator=self.request.user.id))


class SearchChatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering = ("-created_at",)
    http_method_names = ("get",)
    serializer_class = ChatViewSerializer

    def get_queryset(self):
        return Chat.objects.exclude(
            Q(creator=self.request.user.id) | Q(invited=self.request.user.id)
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows message to be viewed or edited.
    """

    permission_classes = (permissions.IsAuthenticated,)
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
        if (
            not self.request.query_params.get("chat")
            and self.request.method == "GET"
        ):
            return Message.objects.none()

        return Message.objects.prefetch_related(
            "chat", "chat__creator", "chat__invited"
        ).filter(
            chat__in=Chat.objects.filter(
                Q(creator=self.request.user.id)
                | Q(invited=self.request.user.id)
            )
        )


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """

    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser,)
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
        if self.request.method == "GET":
            return File.objects.none()

        return File.objects.filter(
            message__in=Message.objects.filter(
                chat__in=Chat.objects.filter(
                    Q(creator=self.request.user.id)
                    | Q(invited=self.request.user.id)
                )
            )
        )
