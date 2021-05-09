from django.contrib.auth import authenticate, login, logout, get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.serializers import LoginSerializer, EmptySerializer, SuccessSerializer, UserRegisterSerializer, \
    UserSerializer


class AuthViewSet(viewsets.GenericViewSet):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer(),
        }
    )
    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(
                permissions.AllowAny,
        ),
        serializer_class=LoginSerializer
    )
    def login(self, request):
        """

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        login(request, user)

        return Response(
            data=UserSerializer(user).data
        )

    @swagger_auto_schema(
        request_body=EmptySerializer,
        responses={
            status.HTTP_200_OK: SuccessSerializer(),
        }
    )
    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(
                permissions.IsAuthenticated,
        ),
        serializer_class=EmptySerializer,
    )
    def logout(self, request):
        """
        Calls Django logout method; Does not work for UserTokenAuth.
        """
        logout(request)

        success_serializer = SuccessSerializer(
            instance={
                "success": "Successfully logged out.",
            }
        )
        return Response(
            data=success_serializer.data,
        )

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer(),
        }
    )
    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(
                permissions.AllowAny,
        ),
        serializer_class=UserRegisterSerializer,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.create_user(**serializer.validated_data)
        user_serializer = UserSerializer(user)
        return Response(
            data=user_serializer.data,
            status=status.HTTP_201_CREATED,
        )
