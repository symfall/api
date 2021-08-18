from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import ChoiceField

from .choices import STATUS
from .models import Chat, File, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "MessengerUserSerializer"
        model = User
        fields = (
            "id",
            "username",
            "email",
            "last_login",
            "first_name",
            "last_name",
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "id",
            "title",
            "creator",
            "invited",
            "is_closed",
            "created_at",
            "updated_at",
        )


class ChatViewSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    invited = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "title",
            "creator",
            "invited",
            "is_closed",
            "created_at",
            "updated_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "chat",
            "text",
            "status",
            "created_at",
            "updated_at",
        )


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            "id",
            "document",
            "message",
            "created_at",
            "updated_at",
        )


class MessageViewSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    chat = ChatViewSerializer()
    status = ChoiceField(choices=STATUS.choices)
    file_set = FileSerializer(many=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "chat",
            "text",
            "status",
            "created_at",
            "updated_at",
            "file_set",
        )
