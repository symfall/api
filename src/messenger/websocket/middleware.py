from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Token checker for WebSocket connections
    """

    async def __call__(self, scope, receive, send):
        try:
            token_key = (
                dict(
                    (
                        x.split("=")
                        for x in scope["query_string"].decode().split("&")
                    )
                )
            ).get("token", None)
        except ValueError:
            token_key = None

        if token_key:
            scope["user"] = await get_user(token_key)
        else:
            raise AuthenticationFailed

        return await super().__call__(scope, receive, send)
