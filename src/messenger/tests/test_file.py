import io
import os
from unittest import skipIf

from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from messenger.tests import (
    DeleteWithoutTokenMixin,
    GetWithoutTokenMixin,
    PostWithoutTokenMixin,
)
from messenger.tests.factory import (
    ChatFactory,
    FileFactory,
    MessageFactory,
    UserFactory,
)

User = get_user_model()


class GetFileViewTest(GetWithoutTokenMixin, APITestCase):
    url_name = "messenger:file-list"

    def test_get_file(self):
        user = UserFactory()
        chat = ChatFactory(creator=user)
        message = MessageFactory(sender=user, chat=chat)
        FileFactory.create_batch(size=25, message=message)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {user.auth_token.key}"
        )
        response = self.client.get(
            reverse("messenger:file-list"), data={"format": "json"}
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["count"], 25)
        self.assertEqual(len(response.json()["results"]), 20)


@skipIf(
    os.getenv("DEPLOYMENT_ARCHITECTURE") == "test", "Don't check in CI/CD flow"
)
class CreateFileViewTest(PostWithoutTokenMixin, APITestCase):
    url_name = "messenger:file-list"

    def test_create_file(self):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)

        user = UserFactory()
        chat = ChatFactory(creator=user)
        message = MessageFactory(sender=user, chat=chat)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {user.auth_token.key}"
        )
        response = self.client.post(
            reverse("messenger:file-list"),
            data={"document": file, "message": message.id},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)


class DeleteFileTest(DeleteWithoutTokenMixin, APITestCase):
    url_name = "messenger:file-detail"

    def test_delete_file(self):
        user = UserFactory()
        chat = ChatFactory(creator=user)
        message = MessageFactory(sender=user, chat=chat)
        file = FileFactory(message=message)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {user.auth_token.key}"
        )
        response = self.client.delete(
            reverse("messenger:file-detail", kwargs={"pk": file.pk})
        )
        self.assertEqual(response.status_code, 204)
