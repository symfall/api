import io
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from messenger.models import Chat, File, Message
from messenger.tests import (
    DeleteWithoutTokenMixin,
    GetWithoutTokenMixin,
    PostWithoutTokenMixin,
)

User = get_user_model()


class GetFileViewTest(GetWithoutTokenMixin, APITestCase):
    url_name = "messenger:file-list"

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
                    }
                ],
            },
            response.json(),
        )

    def test_get_file_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 12345")
        response = self.client.get(
            reverse("messenger:file-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Invalid token."},
            response.json(),
        )

    def test_get_file_with_missing_token(self):
        response = self.client.get(
            reverse("messenger:file-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )


class CreateFileViewTest(PostWithoutTokenMixin, APITestCase):
    url_name = "messenger:file-list"

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

    def tearDown(self) -> None:
        if File.objects.first():
            # run signal to delete physical file
            File.objects.first().delete()

    @freeze_time("1991-02-20 00:00:00")
    def test_create_file(self):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.test_creator.auth_token.key}"
        )
        response = self.client.post(
            reverse("messenger:file-list"),
            data={"document": file, "message": self.test_message.id},
            format="multipart",
        )
        file = File.objects.first()
        self.assertDictEqual(
            {
                "id": file.id,
                "document": urljoin("http://testserver/", file.document.url),
                "message": self.test_message.id,
                "created_at": "1991-02-20T00:00:00Z",
            },
            response.json(),
        )
        self.assertEqual(response.status_code, 201)

    def test_create_file_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 12345")
        response = self.client.post(
            reverse("messenger:file-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Invalid token."},
            response.json(),
        )

    def test_create_file_with_missing_token(self):
        response = self.client.post(
            reverse("messenger:file-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )


class DeleteFileTest(DeleteWithoutTokenMixin, APITestCase):
    url_name = "messenger:file-detail"

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
