from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.base_user import BaseUserManager
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "last_login",
            "first_name",
            "last_name",
            "auth_token",
        )


class EmptySerializer(serializers.Serializer):  # pylint: disable=W0223
    pass


class SuccessSerializer(serializers.Serializer):  # pylint: disable=W0223
    success = serializers.CharField(default="All right")


class LoginSerializer(serializers.Serializer):  # pylint: disable=W0223
    username = serializers.CharField(max_length=32, required=True)
    password = serializers.CharField(required=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )

    @staticmethod
    def validate_username(value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("Username is already taken")
        return BaseUserManager.normalize_email(value)

    @staticmethod
    def validate_password(value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):  # pylint:disable=W0223
    """
    Password Changer
    """

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(
                "Current password does not match"
            )
        return value

    @staticmethod
    def validate_new_password(value):
        password_validation.validate_password(value)
        return value
