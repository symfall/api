from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from messenger.tests import (
    DeleteWithoutTokenMixin,
    GetWithoutTokenMixin,
    PostWithoutTokenMixin,
    PutWithoutTokenMixin,
)
from messenger.tests.factory import ChatFactory, MessageFactory, UserFactory

User = get_user_model()


class GetMessageViewTest(GetWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-list"

    def test_get_message(self):
        user = UserFactory()
        chat = ChatFactory(creator=user)
        MessageFactory.create_batch(size=25, chat=chat, sender=user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {user.auth_token.key}"
        )
        response = self.client.get(
            reverse("messenger:message-list"),
            data={"chat": chat.id, "format": "json"},
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["count"], 25)
        self.assertEqual(len(response.json()["results"]), 20)


class CreateMessageViewTest(PostWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-list"

    def test_create_message(self):
        chat = ChatFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {chat.creator.auth_token.key}"
        )
        response = self.client.post(
            reverse("messenger:message-list"),
            data={
                "sender": chat.creator.pk,
                "chat": chat.pk,
                "text": "add new hello world",
                "status": 1,
            },
        )
        self.assertEqual(response.status_code, 201)


class DeleteMessageViewTest(DeleteWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-detail"

    def test_delete_message(self):
        message = MessageFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {message.chat.creator.auth_token.key}"
        )
        response = self.client.delete(
            reverse(
                "messenger:message-detail",
                kwargs={"pk": message.pk},
            )
        )
        self.assertEqual(response.status_code, 204)


class EditMessageViewTest(PutWithoutTokenMixin, APITestCase):
    url_name = "messenger:message-detail"

    def test_edit_message(self):
        message = MessageFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {message.chat.creator.auth_token.key}"
        )
        response = self.client.put(
            reverse(
                "messenger:message-detail",
                kwargs={"pk": message.pk},
            ),
            data={
                "sender": message.chat.creator.pk,
                "chat": message.chat.pk,
                "text": "edit hello world",
            },
        )
        self.assertEqual(response.status_code, 200)
