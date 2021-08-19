from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from messenger.models import Chat, Message
from messenger.tests import (
    DeleteWithoutTokenMixin,
    GetWithoutTokenMixin,
    PostWithoutTokenMixin,
    PutWithoutTokenMixin,
)

User = get_user_model()


class GetMessageViewTest(GetWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-list"

    @freeze_time("1991-02-20 00:00:00")
    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username="test_sender", password="1234567"
        )
        Token.objects.create(user=self.test_sender)
        self.test_chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_sender,
        )
        self.test_message = Message.objects.create(
            sender=self.test_sender,
            chat=self.test_chat,
            text="hello world",
            status=2,
        )

    @freeze_time("1991-02-20 00:00:00")
    def test_get_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.get(
            reverse("messenger:message-list"),
            data={"chat": str(self.test_chat.id), "format": "json"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "sender": {
                            "id": self.test_sender.id,
                            "email": "",
                            "first_name": "",
                            "last_login": None,
                            "last_name": "",
                            "username": "test_sender",
                        },
                        "chat": {
                            "id": self.test_chat.id,
                            "created_at": "1991-02-20T00:00:00Z",
                            "creator": {
                                "id": self.test_sender.id,
                                "email": "",
                                "first_name": "",
                                "last_login": None,
                                "last_name": "",
                                "username": "test_sender",
                            },
                            "invited": [],
                            "is_closed": False,
                            "title": "test-chat",
                            "updated_at": "1991-02-20T00:00:00Z",
                        },
                        "id": self.test_message.id,
                        "text": "hello world",
                        "status": 2,
                        "created_at": "1991-02-20T00:00:00Z",
                        "updated_at": "1991-02-20T00:00:00Z",
                        "file_set": [],
                    }
                ],
            },
            response.json(),
        )


class CreateMessageViewTest(PostWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-list"

    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username="test_add_sender", password="1234567"
        )
        Token.objects.create(user=self.test_sender)
        self.test_chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_sender,
        )
        self.message = {
            "sender": str(self.test_sender.pk),
            "chat": str(self.test_chat.pk),
            "text": "add new hello world",
            "status": 1,
        }

    def test_create_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.post(
            reverse("messenger:message-list"),
            data=self.message,
        )
        self.assertEqual(response.status_code, 201)


class DeleteMessageViewTest(DeleteWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-detail"

    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username="test_delete_sender", password="1234567"
        )
        Token.objects.create(user=self.test_sender)
        self.test_chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_sender,
        )
        self.test_message = Message.objects.create(
            sender=self.test_sender,
            chat=self.test_chat,
            text="delete hello world",
            status=2,
        )
        self.instance = self.test_message

    def test_delete_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.delete(
            reverse(
                "messenger:message-detail",
                kwargs={"pk": self.test_message.pk},
            )
        )
        self.assertEqual(response.status_code, 204)


class EditMessageViewTest(PutWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-detail"

    @freeze_time("1991-02-20 00:00:00")
    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username="test_edit_sender", password="1234567"
        )
        Token.objects.create(user=self.test_sender)
        self.test_chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_sender,
        )
        self.test_message = Message.objects.create(
            sender=self.test_sender,
            chat=self.test_chat,
            text="hello world",
            status=2,
        )
        self.edit_message = {
            "sender": str(self.test_sender.pk),
            "chat": str(self.test_chat.pk),
            "text": "edit hello world",
        }

    def test_edit_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.put(
            reverse(
                "messenger:message-detail",
                kwargs={"pk": str(self.test_message.pk)},
            ),
            data=self.edit_message,
        )
        self.assertEqual(response.status_code, 200)
