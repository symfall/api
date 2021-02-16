import json
from unittest import skip

from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APITestCase
from .models import User, Chat, Message


# -> HealthCheckView test
class HealthCheckViewTest(APITestCase):

    def test_health_check(self):
        """
        Method for viewing health check in json format
        """
        response = self.client.get('/health_check', data={'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'Cache backend: default': 'working',
            'DatabaseBackend': 'working',
            'DiskUsage': 'working',
            'MemoryUsage': 'working',
            'MigrationsHealthCheck': 'working'},
            response.json()
        )


# -> Chat test's
class GetChatViewTest(APITestCase):

    @freeze_time('1991-02-20 00:00:00')
    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username='test_creator',
            password='12345'
        )
        Chat.objects.create(
            title='test-chat',
            creator=self.test_creator,
        )

    @freeze_time('1991-02-20 00:00:00')
    def test_get_chat(self):
        self.client.login(username='test_creator', password='12345')
        response = self.client.get(
            reverse('api:chat-list'),
            data={'format': 'json'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'title': 'test-chat',
                'creator': {
                    'email': '',
                    'first_name': '',
                    'groups': [],
                    'last_login': '1991-02-20T00:00:00Z',
                    'last_name': '',
                    'username': 'test_creator'
                },
                'invited': [],
                'is_closed': False,
                'created_at': '1991-02-20T00:00:00Z',
                'updated_at': '1991-02-20T00:00:00Z',
            }]
        }, response.json())


class AddChatViewTest(APITestCase):

    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username='test_creator_create',
            password='12345'
        )
        self.test_invited = User.objects.create_user(
            username='test_invited_create',
            password='67890'
        )
        self.chat = {
            'title': 'test-chat-create_201',
            'creator': self.test_creator.pk,
            'invited': [self.test_creator.pk, self.test_invited.pk],
            'is_closed': True
        }

    def test_create_chat(self):
        self.client.login(username='test_creator_create', password='12345')
        response = self.client.post(
            reverse('api:chat-list'),
            data=json.dumps(self.chat),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)


class DeleteChatViewTest(APITestCase):

    def setUp(self):
        self.test_creator = User.objects.create_user(
            username='test_creator_delete',
            password='18892'
        )
        self.test_chat_delete = Chat.objects.create(
            title='test-chat',
            creator=self.test_creator
        )

    def test_delete_chat(self):
        self.client.login(username='test_creator_delete', password='18892')
        response = self.client.delete(
            reverse('api:chat-detail', kwargs={'pk': self.test_chat_delete.pk}))
        self.assertEqual(response.status_code, 204)


class EditChatViewTest(APITestCase):

    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username='test_creator',
            password='1234567'
        )
        self.test_invited = User.objects.create_user(
            username='test_invited',
            password='234567890'
        )
        self.test_chat_edit = Chat.objects.create(
            title='test-chat-update',
            creator=self.test_creator
        )
        self.edit_chat = {
            'title': 'test_chat_updateV2.',
            'creator': self.test_creator.pk,
            'invited': [self.test_creator.pk, self.test_invited.pk]
        }

    def test_edit_chat(self):
        self.client.login(username='test_creator', password='1234567')
        response = self.client.put(
            reverse('api:chat-detail', kwargs={'pk': self.test_chat_edit.pk}),
            data=json.dumps(self.edit_chat),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


class GetUserViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user',
            password='1234567',
            email='test_user@gmail.com',
        )

    @freeze_time('1991-02-20 00:00:00')
    def test_get_user(self):
        self.client.login(username='test_user', password='1234567')
        response = self.client.get(reverse('api:user-list'), data={'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results':
                    [
                        {
                            'username': 'test_user',
                            'email': 'test_user@gmail.com',
                            'groups': [],
                            'last_login': '1991-02-20T00:00:00Z',
                            'first_name': '',
                            'last_name': ''
                        }
                    ]
            }, response.json()
        )


@skip('Test create')
class AddUserViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = {
            'username': 'test_add_user',
            'password': '1234567',
            'email': 'test_add_user@gmail.com'
        }

    def test_add_user(self):
        self.client.login(username='test_add_user', password='1234567')
        response = self.client.post(
            reverse('api:user-list'),
            data=json.dumps(self.user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)


class DeleteUserViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_delete_user',
            password='1234567',
            email='test_delete_user@gmail.com',
        )

    def test_delete_user(self):
        self.client.login(username='test_delete_user', password='1234567')
        response = self.client.delete(
            reverse('api:user-detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 204)


class EditUserViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_edit_user',
            password='1234567',
            email='test_edit_user@gmail.com',
        )

        self.edit_user = {
            'username': 'test_user_edit',
            'password': '3214532',
            'email': 'test_user_edit@gmail.com'
        }

    def test_edit_user(self):
        self.client.login(username='test_edit_user', password='1234567')
        response = self.client.put(
            reverse('api:user-detail', kwargs={'pk': self.user.pk}),
            json.dumps(self.edit_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


# -> Message tests
class GetMessageViewTest(APITestCase):

    @freeze_time('1991-02-20 00:00:00')
    def setUp(self) -> None:
        test_sender = User.objects.create_user(
            username='test_sender',
            password='1234567'
        )
        test_chat = Chat.objects.create(
            title='test-chat',
            creator=test_sender,
        )
        self.test_message = Message.objects.create(
            sender=test_sender,
            chat=test_chat,
            message='hello world',
            status=2
        )

    @freeze_time('1991-02-20 00:00:00')
    def test_get_message(self):
        self.maxDiff = None
        self.client.login(username='test_sender', password='1234567')
        response = self.client.get(reverse('api:message-list'), data={'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'sender': {
                    'email': '',
                    'first_name': '',
                    'groups': [],
                    'last_login': '1991-02-20T00:00:00Z',
                    'last_name': '',
                    'username': 'test_sender'
                },
                'chat': {'created_at': '1991-02-20T00:00:00Z',
                         'creator': {'email': '',
                                     'first_name': '',
                                     'groups': [],
                                     'last_login': '1991-02-20T00:00:00Z',
                                     'last_name': '',
                                     'username': 'test_sender'},
                         'invited': [],
                         'is_closed': False,
                         'title': 'test-chat',
                         'updated_at': '1991-02-20T00:00:00Z'},
                'message': 'hello world',
                'status': 'not viewed',
                'created_at': '1991-02-20T00:00:00Z',
                'updated_at': '1991-02-20T00:00:00Z'
            }]
        }, response.json())


class CreateMessageViewTest(APITestCase):

    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username='test_add_sender',
            password='1234567'
        )
        self.test_chat = Chat.objects.create(
            title='test-chat',
            creator=self.test_sender,
        )
        self.message = {
            'sender': self.test_sender.pk,
            'chat': self.test_chat.pk,
            'message': 'add new hello world',
            'status': 1
        }

    def test_create_chat(self):
        self.client.login(username='test_add_sender', password='1234567')
        response = self.client.post(
            reverse('api:message-list'),
            data=json.dumps(self.message),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)


class DeleteMessageViewTest(APITestCase):

    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username='test_delete_sender',
            password='1234567'
        )
        self.test_chat = Chat.objects.create(
            title='test-chat',
            creator=self.test_sender,
        )
        self.test_delete_message = Message.objects.create(
            sender=self.test_sender,
            chat=self.test_chat,
            message='delete hello world',
            status=2
        )

    def test_delete_message(self):
        self.client.login(username='test_delete_sender', password='1234567')
        response = self.client.delete(
            reverse('api:message-detail', kwargs={'pk': self.test_delete_message.pk})
        )
        self.assertEqual(response.status_code, 204)


class EditMessageViewTest(APITestCase):

    @freeze_time('1991-02-20 00:00:00')
    def setUp(self) -> None:
        self.test_sender = User.objects.create_user(
            username='test_edit_sender',
            password='1234567'
        )
        self.test_chat = Chat.objects.create(
            title='test-chat',
            creator=self.test_sender,
        )
        self.test_edit_message = Message.objects.create(
            sender=self.test_sender,
            chat=self.test_chat,
            message='hello world',
            status=2
        )
        self.edit_message = {
            'sender': self.test_sender.pk,
            'chat': self.test_chat.pk,
            'message': 'edit hello world',
            'status': 1
        }

    def test_edit_message(self):
        self.client.login(username='test_edit_sender', password='1234567')
        response = self.client.put(
            reverse('api:message-detail', kwargs={'pk': self.test_edit_message.pk}),
            data=json.dumps(self.edit_message),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
