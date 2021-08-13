import json

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class AddUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user",
            password="1234567",
            email="test_user@gmail.com",
        )

    def test_user_logout(self):
        response = self.client.post(
            reverse("api:auth-logout"),
            content_type="application/json",
        )
        self.assertDictEqual(
            response.data,
            {"success": "Successfully logged out"},
        )

    def test_user_login(self):
        response = self.client.post(
            path=reverse("api:auth-login"),
            data=json.dumps(
                {
                    "username": "test_user",
                    "password": "1234567",
                    "email": "test_user@gmail.com",
                }
            ),
            content_type="application/json",
        )
        self.assertDictEqual(
            response.data,
            {
                "id": self.user.id,
                "auth_token": None,
                "username": "test_user",
                "email": "test_user@gmail.com",
                "last_login": None,
                "first_name": "",
                "last_name": "",
            },
        )

    def test_user_register(self):
        response = self.client.post(
            path=reverse("api:auth-register"),
            data=json.dumps(
                {
                    "username": "username",
                    "password": "1234567!",
                    "email": "test_user_register@mail.com",
                }
            ),
            content_type="application/json",
        )
        registered_user = User.objects.get(username="username")
        self.assertDictEqual(
            response.data,
            {
                "id": registered_user.id,
                "auth_token": None,
                "username": "username",
                "email": "test_user_register@mail.com",
                "last_login": None,
                "first_name": "",
                "last_name": "",
            },
        )

    def test_user_activation(self):
        user_id_b64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(user=self.user)

        response = self.client.get(
            path=reverse(
                "api:auth-activation",
                kwargs={
                    "user_id_b64": user_id_b64,
                    "token": token,
                },
            ),
            content_type="application/json",
        )
        self.assertDictEqual(
            response.data,
            {"success": "Successfully activated account"},
        )
