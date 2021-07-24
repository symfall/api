import json

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from freezegun import freeze_time
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class GetUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user",
            password="1234567",
            email="test_user@gmail.com",
        )

    @freeze_time("1991-02-20 00:00:00")
    def test_get_user(self):
        self.client.login(
            username="test_user",
            password="1234567",
        )
        response = self.client.get(
            path=reverse("api:user-list"),
            data={"format": "json"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "username": "test_user",
                        "email": "test_user@gmail.com",
                        "last_login": "1991-02-20T00:00:00Z",
                        "first_name": "",
                        "last_name": "",
                    }
                ],
            },
            response.json(),
        )


class DeleteUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_delete_user",
            password="1234567",
            email="test_delete_user@gmail.com",
        )

    def test_delete_user(self):
        self.client.login(
            username="test_delete_user",
            password="1234567",
        )
        response = self.client.delete(
            path=reverse("api:user-detail", kwargs={"pk": self.user.pk}),
        )
        self.assertEqual(response.status_code, 204)


class EditUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_edit_user",
            password="1234567",
            email="test_edit_user@gmail.com",
        )

        self.edit_user = {
            "username": "test_user_edit",
            "password": "3214532",
            "email": "test_user_edit@gmail.com",
        }

    def test_edit_user(self):
        self.client.login(username="test_edit_user", password="1234567")
        response = self.client.put(
            reverse("api:user-detail", kwargs={"pk": self.user.pk}),
            json.dumps(self.edit_user),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)


class AddUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user",
            password="1234567",
            email="test_user@gmail.com",
        )

    def test_user_logout(self):
        self.client.login(username="test_user", password="1234567")
        response = self.client.get(
            reverse("api:auth-logout"),
            content_type="application/json",
        )
        self.assertEqual(
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
        self.assertEqual(
            response.data,
            {
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
        self.assertEqual(
            response.data,
            {
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
        self.assertEqual(
            response.data,
            {"success": "Successfully activated account"},
        )
