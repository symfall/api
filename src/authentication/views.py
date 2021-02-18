from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from messenger.serializers import LoginSerializer, UserSerializer, EmptySerializer


class AuthViewSet(viewsets.GenericViewSet):

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
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data)

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

        return Response({"success": "Successfully logged out."})
