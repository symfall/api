import os
from unittest import skipIf

from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from messenger.tests import (
    DeleteWithoutTokenMixin,
    GetWithoutTokenMixin,
    PostWithoutTokenMixin,
    PutWithoutTokenMixin,
)
from messenger.tests.factory import ChatFactory, MessageFactory, UserFactory
from messenger.websocket.handler import get_ws_application


class GetChatViewTest(GetWithoutTokenMixin, APITestCase):
    url_name = "messenger:chat-list"

    def test_get_chat(self):
        user = UserFactory()
        ChatFactory.create_batch(size=25, creator=user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {user.auth_token.key}"
        )
        response = self.client.get(
            reverse("messenger:chat-list"),
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["count"], 25)
        self.assertEqual(len(response.json()["results"]), 20)


class AddChatViewTest(PostWithoutTokenMixin, APITestCase):
    url_name = "messenger:chat-list"

    def test_create_chat(self):
        creator = UserFactory()
        invited_user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {creator.auth_token.key}"
        )
        response = self.client.post(
            reverse("messenger:chat-list"),
            data={
                "title": "test-chat-create_201",
                "creator": creator.pk,
                "invited": [invited_user.pk],
            },
        )
        self.assertEqual(response.status_code, 201)


class DeleteChatViewTest(DeleteWithoutTokenMixin, APITestCase):
    url_name = "messenger:chat-detail"

    def test_delete_chat(self):
        chat = ChatFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {chat.creator.auth_token.key}"
        )
        response = self.client.delete(
            reverse("messenger:chat-detail", args=(chat.id,))
        )
        self.assertEqual(response.status_code, 204)


class EditChatViewTest(PutWithoutTokenMixin, APITestCase):
    url_name = "messenger:chat-detail"

    def test_edit_chat(self):
        chat = ChatFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {chat.creator.auth_token.key}"
        )
        response = self.client.put(
            reverse(
                "messenger:chat-detail",
                kwargs={"pk": chat.pk},
            ),
            data={
                "title": "test_chat_updateV2.",
                "creator": chat.creator.pk,
                "invited": [chat.creator.pk],
            },
        )
        self.assertEqual(response.status_code, 200)


@skipIf(
    os.getenv("DEPLOYMENT_ARCHITECTURE") == "test", "Don't check in CI/CD flow"
)
class ChatConsumerTest(TestCase):
    @sync_to_async
    def create_message(self, chat=None):
        if chat:
            self.message = MessageFactory(chat=chat)
        else:
            self.message = MessageFactory()

    async def test_my_consumer(self):
        await self.create_message()
        communicator = WebsocketCommunicator(
            application=get_ws_application(),
            path=f"/ws/chat/{self.message.chat.id}?"
            f"token={self.message.chat.creator.auth_token.key}",
        )
        await communicator.connect()
        await self.create_message(chat=self.message.chat)
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message["id"], self.message.id)
        await communicator.disconnect()

    async def test_check_if_token_missing(self):
        await self.create_message()
        communicator = WebsocketCommunicator(
            application=get_ws_application(),
            path=f"/ws/chat/{self.message.chat.id}",
        )
        with self.assertRaises(AuthenticationFailed):
            await communicator.connect()
