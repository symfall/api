from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.serializers import (EmptySerializer, LoginSerializer,
                                        SuccessSerializer,
                                        UserRegisterSerializer, UserSerializer)
from authentication.tokens import account_activation_token

User = get_user_model()


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
        Endpoint which check username and password
        If these params are right and username exists in database
        and password is correct for the username than we will login user to the system
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
                "success": "",
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
    def activation(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # checking if the user exists, if the token is valid.
        if user is not None and account_activation_token.check_token(user, token):
            # if valid set active true
            user.is_active = True
            # set signup_confirmation true
            user.profile.signup_confirmation = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'activation_invalid.html')
