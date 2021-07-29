from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.emails import send_email
from authentication.serializers import (
    AuthUserSerializer,
    EmptySerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    SuccessSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    """
    Authentication ViewSet class
    """

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: LoginSerializer(),
        },
    )
    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(permissions.AllowAny,),
        serializer_class=LoginSerializer,
    )
    def login(self, request):
        """
        Endpoint which check username and password
        If these params are right and username exists in database
        and password is correct for the username than
        we will login user to the system
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            raise serializers.ValidationError(
                "Invalid username/password. Please try again!"
            )
        data = UserSerializer(user).data

        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: SuccessSerializer(),
        },
    )
    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=EmptySerializer,
    )
    def logout(self, request):
        """
        Calls Django logout method;
        Does not work for UserTokenAuth.
        """
        logout(request)

        success_serializer = SuccessSerializer(
            instance={
                "success": "Successfully logged out",
            }
        )
        return Response(
            data=success_serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=PasswordChangeSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: EmptySerializer(),
        },
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=PasswordChangeSerializer,
    )
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            status.HTTP_200_OK: UserRegisterSerializer(),
        },
    )
    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(permissions.AllowAny,),
        serializer_class=UserRegisterSerializer,
    )
    def register(self, request):
        """
        Register user with email, name and password data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_model().objects.create_user(
            **serializer.validated_data,
            is_active=False,
        )
        data = UserSerializer(user).data

        user_id = urlsafe_base64_encode(force_bytes(user.pk))

        activate_url = f"{settings.FRONT_URL}/{user_id}/{default_token_generator.make_token(user=user)}"
        send_email(
            recipient_list=[user.email],
            activate_url=activate_url,
        )

        return Response(data=data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: AuthUserSerializer(),
        }
    )
    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(permissions.AllowAny,),
        serializer_class=UserRegisterSerializer,
        url_path=r"activation/(?P<user_id_b64>[\d\w-]+)/(?P<token>[\d\w-]+)",
    )
    def activation(self, request, user_id_b64, token):
        try:
            uid = force_str(urlsafe_base64_decode(user_id_b64))
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            message = {"success": "Successfully activated account"}
        else:
            message = {"error": "Activation failed"}

        return Response(data=message)
