from django.contrib.auth import get_user_model
from rest_framework import serializers

from messenger.choice import ChoiceField
from .choices import STATUS
from .models import Chat, Message, File, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'last_login',
            'first_name',
            'last_name',
        )


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = (
            'title',
            'creator',
            'invited',
            'is_closed',
        )


class ChatViewSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    invited = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = (
            'title',
            'creator',
            'invited',
            'is_closed',
            'created_at',
            'updated_at',
        )


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'sender',
            'chat',
            'message',
            'status',
        )


class MessageViewSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    chat = ChatViewSerializer()
    status = ChoiceField(choices=STATUS.choices)

    class Meta:
        model = Message
        fields = (
            'sender',
            'chat',
            'message',
            'status',
            'created_at',
            'updated_at',
        )


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            'document',
            'message',
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)


class EmptySerializer(serializers.Serializer):

    success = serializers.CharField(default='Successfully logged out.')

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'first_name', 'last_name', 'gender', 'tshirt_size', 'phone_number']
#
#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Email is already taken.")
#         return UserManager.normalize_email(value)
#
#
# class AuthUserSerializer(UserSerializer):
#     auth_token = serializers.SerializerMethodField()
#
#     class Meta(UserSerializer.Meta):
#         fields = UserSerializer.Meta.fields + ['auth_token']
#
#     def get_auth_token(self, obj):
#         return tokens.get_token_for_user(obj, "authentication")