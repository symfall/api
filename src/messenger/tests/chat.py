from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from messenger.models import Chat

User = get_user_model()


class GetChatViewTest(APITestCase):
    @freeze_time("1991-02-20 00:00:00")
    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username="test_creator",
            password="12345",
            email="test_user@gmail.com",
        )
        Token.objects.create(user=self.test_creator)
        self.chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_creator,
        )

    @freeze_time("1991-02-20 00:00:00")
    def test_get_chat(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.get(
            reverse("api:chat-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, 200)  # pylint: disable=E1101
        self.assertDictEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.chat.pk,
                        "title": "test-chat",
                        "creator": {
                            "id": self.test_creator.id,
                            "email": "test_user@gmail.com",
                            "first_name": "",
                            "last_login": None,
                            "last_name": "",
                            "username": "test_creator",
                        },
                        "invited": [],
                        "is_closed": False,
                        "created_at": "1991-02-20T00:00:00Z",
                        "updated_at": "1991-02-20T00:00:00Z",
                    }
                ],
            },
            response.json(),  # pylint: disable=E1101
        )


class AddChatViewTest(APITestCase):
    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username="test_creator_create", password="12345"
        )
        Token.objects.create(user=self.test_creator)
        self.test_invited = User.objects.create_user(
            username="test_invited_create", password="67890"
        )
        self.chat = {
            "title": "test-chat-create_201",
            "creator": self.test_creator.pk,
            "invited": [self.test_creator.pk, self.test_invited.pk],
            "is_closed": True,
        }

    def test_create_chat(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.post(
            reverse("api:chat-list"),
            data=self.chat,
        )
        self.assertEqual(response.status_code, 201)


class DeleteChatViewTest(APITestCase):
    def setUp(self):
        self.test_creator = User.objects.create_user(
            username="test_creator_delete", password="18892"
        )
        Token.objects.create(user=self.test_creator)
        self.test_chat_delete = Chat.objects.create(
            title="test-chat", creator=self.test_creator
        )

    def test_delete_chat(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.delete(
            reverse("api:chat-detail", args=(str(self.test_chat_delete.pk),))
        )
        self.assertEqual(response.status_code, 204)


class EditChatViewTest(APITestCase):
    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username="test_creator", password="1234567"
        )
        Token.objects.create(user=self.test_creator)
        self.test_invited = User.objects.create_user(
            username="test_invited", password="234567890"
        )
        self.test_chat_edit = Chat.objects.create(
            title="test-chat-update", creator=self.test_creator
        )
        self.edit_chat = {
            "title": "test_chat_updateV2.",
            "creator": self.test_creator.pk,
            "invited": [self.test_creator.pk, self.test_invited.pk],
        }

    def test_edit_chat(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.put(
            reverse(
                "api:chat-detail", kwargs={"pk": str(self.test_chat_edit.pk)}
            ),
            data=self.edit_chat,
        )
        self.assertEqual(response.status_code, 200)
