from unittest import mock

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.tests.factory import UserFactory


class AddUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_user_logout(self):
        response = self.client.post(
            reverse("authentication:auth-logout"),
            content_type="application/json",
        )
        self.assertDictEqual(
            response.data,
            {"success": "Successfully logged out"},
        )

    def test_user_login(self):
        response = self.client.post(
            path=reverse("authentication:auth-login"),
            data={
                "username": self.user.username,
                "password": "password",
                "email": self.user.email,
            },
        )
        self.assertEqual(response.data["id"], self.user.id)

    @mock.patch("authentication.api.v1.views.send_activation_email")
    def test_user_register_without_activate_url(self, send_mail_mocked):
        response = self.client.post(
            path=reverse("authentication:auth-register"),
            data={
                "username": "username",
                "password": "1234567!",
                "email": "test_user_register@mail.com",
            },
            HTTP_Origin="http://testserver",
        )
        self.assertEqual(response.data["username"], "username")
        self.assertRegex(
            send_mail_mocked.call_args.kwargs["activate_url"],
            r"http://testserver/(.+)",
        )

    @mock.patch("authentication.api.v1.views.send_activation_email")
    def test_user_register_with_activate_url(self, send_mail_mocked):
        response = self.client.post(
            path=reverse("authentication:auth-register"),
            data={
                "username": "username",
                "password": "1234567!",
                "email": "test_user_register@mail.com",
                "activate_url": "http://test.com/activate",
            },
        )
        self.assertEqual(response.data["username"], "username")
        self.assertRegex(
            send_mail_mocked.call_args.kwargs["activate_url"],
            r"http://test.com/activate(.+)",
        )

    def test_user_activation(self):
        user_id_b64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(user=self.user)

        response = self.client.get(
            path=reverse(
                "authentication:auth-activate",
                kwargs={
                    "user_id_b64": user_id_b64,
                    "token": token,
                },
            )
        )
        self.assertDictEqual(
            response.data,
            {
                "success": "Successfully activated account",
                "token": self.user.auth_token.key,
            },
        )
