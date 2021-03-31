from rest_framework import serializers

from authentication.serializers import UserSerializer
from messenger.choice import ChoiceField
from .choices import STATUS
from .models import Chat, Message, File


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "title",
            "creator",
            "invited",
            "is_closed",
        )


class ChatViewSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    invited = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = (
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
            "sender",
            "chat",
            "message",
            "status",
        )


class MessageViewSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    chat = ChatViewSerializer()
    status = ChoiceField(choices=STATUS.choices)

    class Meta:
        model = Message
        fields = (
            "sender",
            "chat",
            "message",
            "status",
            "created_at",
            "updated_at",
        )


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            "document",
            "message",
        )
