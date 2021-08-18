from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from messenger.models import Chat, File, Message

User = get_user_model()


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
            text="test-message",
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
            reverse("messenger:file-list"), data={"format": "json"}
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
            text="test-message",
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
            reverse(
                "messenger:file-detail", kwargs={"pk": str(self.test_file.pk)}
            )
        )
        self.assertEqual(response.status_code, 204)
