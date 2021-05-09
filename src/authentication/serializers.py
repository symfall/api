from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "last_login",
            "first_name",
            "last_name",
        )


class EmptySerializer(serializers.Serializer):
    pass


class SuccessSerializer(serializers.Serializer):
    success = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return User.objects.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


# class StudentViewSet(ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     pagination_class = PageNumberPagination
#     filter_backends = (DjangoFilterBackend,filters.OrderingFilter)
#     filter_class = StudentFilter
#     ordering = ['name']