import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from messenger.models import Chat, File, Message

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
            data=json.dumps(self.chat),
            content_type="application/json",
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
            data=json.dumps(self.edit_chat),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)


# -> Message tests
class GetMessageViewTest(APITestCase):
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
            message="hello world",
            status=2,
        )

    @freeze_time("1991-02-20 00:00:00")
    def test_get_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.get(
            reverse("api:message-list"),
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
                        "message": "hello world",
                        "status": "not viewed",
                        "created_at": "1991-02-20T00:00:00Z",
                        "updated_at": "1991-02-20T00:00:00Z",
                        "file_set": [],
                    }
                ],
            },
            response.json(),
        )


class CreateMessageViewTest(APITestCase):
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
            "message": "add new hello world",
            "status": 1,
        }

    def test_create_chat(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.post(
            reverse("api:message-list"),
            data=json.dumps(self.message),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)


class DeleteMessageViewTest(APITestCase):
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
            message="delete hello world",
            status=2,
        )

    def test_delete_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.delete(
            reverse(
                "api:message-detail",
                kwargs={"pk": self.test_message.pk},
            )
        )
        self.assertEqual(response.status_code, 204)


class EditMessageViewTest(APITestCase):
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
            message="hello world",
            status=2,
        )
        self.edit_message = {
            "sender": str(self.test_sender.pk),
            "chat": str(self.test_chat.pk),
            "message": "edit hello world",
        }

    def test_edit_message(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_sender.auth_token.key}"
        )
        response = self.client.put(
            reverse(
                "api:message-detail",
                kwargs={"pk": str(self.test_message.pk)},
            ),
            data=json.dumps(self.edit_message),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)


class GetFileViewTest(APITestCase):
    @freeze_time("1991-02-20 00:00:00")
    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username="test_creator",
            password="12345",
        )
        Token.objects.create(user=self.test_creator)
        self.test_chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_creator,
        )
        self.test_message = Message.objects.create(
            sender=self.test_creator,
            chat=self.test_chat,
            message="test-message",
            status=2,
        )
        self.test_file = File.objects.create(
            document=None,
            message=self.test_message,
        )

    def test_get_file(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.get(
            reverse("api:file-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.test_file.id,
                        "document": None,
                        "message": self.test_message.id,
                        "created_at": "1991-02-20T00:00:00Z",
                        "updated_at": "1991-02-20T00:00:00Z",
                    }
                ],
            },
            response.json(),
        )


class DeleteFileTest(APITestCase):
    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username="test_creator",
            password="12345",
        )
        Token.objects.create(user=self.test_creator)
        self.test_chat = Chat.objects.create(
            title="test-chat",
            creator=self.test_creator,
        )
        self.test_message = Message.objects.create(
            sender=self.test_creator,
            chat=self.test_chat,
            message="test-message",
            status=2,
        )
        self.test_file = File.objects.create(
            document=None,
            message=self.test_message,
        )

    def test_delete_file(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.delete(
            reverse("api:file-detail", kwargs={"pk": str(self.test_file.pk)})
        )
        self.assertEqual(response.status_code, 204)
