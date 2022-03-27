from urllib.parse import ParseResult, parse_qsl, urlparse, urlunparse

from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlencode,
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from authentication.emails import send_activation_email
from authentication.serializers import (
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
        responses={
            status.HTTP_200_OK: UserSerializer(),
        },
    )
    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=EmptySerializer,
        pagination_class=None,
    )
    def user(self, request):
        """Retrieves basic data of current user

        Args:
            request: Django Request Instance

        Returns:
            response: Response
        """
        user_serializer = UserSerializer(request.user)

        return Response(
            data=user_serializer.data,
            status=status.HTTP_200_OK,
        )

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
        Calls Django login method

        Args:
            request: Django Request Instance

        Returns:
            response: Response

        Raises:
            ValidationError: If serializer validation fails
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
        user_serializer = UserSerializer(user)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: SuccessSerializer(),
        },
    )
    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(permissions.AllowAny,),
        serializer_class=EmptySerializer,
        pagination_class=None,
    )
    def logout(self, request):
        """Calls Django logout method;

        Does not work for UserTokenAuth.

        Args:
            request: Django Request Instance

        Returns:
            response: Response
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
        """Register user with email, name and password data

        Args:
            request: Django Request Instance

        Returns:
            response: Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        activate_url = None
        if serializer.validated_data.get("activate_url"):
            activate_url = serializer.validated_data.pop("activate_url")

        user = get_user_model().objects.create_user(
            **serializer.validated_data,
            is_active=False,
        )
        user_serializer = UserSerializer(user)

        params = {
            "user_id_b64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user=user),
        }

        if activate_url:
            url_parts = list(urlparse(activate_url))
            query = dict(parse_qsl(url_parts[4]))
            query.update(params)
            url_parts[4] = urlencode(query)
            activate_url = urlunparse(url_parts)
        else:
            url_parts = urlparse(request.build_absolute_uri())
            parse_result = ParseResult(
                scheme=url_parts.scheme,
                netloc=url_parts.hostname,
                path=reverse(
                    "authentication:auth-activate",
                    kwargs=params,
                ),
                params=url_parts.params,
                query=None,
                fragment=url_parts.fragment,
            )
            activate_url = parse_result.geturl()

        send_activation_email(
            recipient_list=[user.email],
            activate_url=activate_url,
        )
        return Response(
            data=user_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: UserSerializer(),
        }
    )
    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(permissions.AllowAny,),
        serializer_class=UserRegisterSerializer,
        url_path=r"activate/(?P<user_id_b64>[\d\w-]+)/(?P<token>[\d\w-]+)",
        pagination_class=None,
    )
    def activate(self, request, user_id_b64, token):
        """Activate registered user account

        Args:
            request: Django Request Instance
            user_id_b64: User ID in base 64
            token: Token

        Returns:
            response: Response
        """
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

            token, _ = Token.objects.get_or_create(user=user)

            message, status_code = {
                "success": "Successfully activated account",
                "token": token.key,
            }, status.HTTP_200_OK
        else:
            message, status_code = {
                "error": "Activation failed"
            }, status.HTTP_400_BAD_REQUEST

        return Response(data=message, status=status_code)
