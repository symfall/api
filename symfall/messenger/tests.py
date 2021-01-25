import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User, Chat


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


class GetChatViewTest(APITestCase):

    def setUp(self) -> None:
        self.test_creator = User.objects.create_user(
            username='test_creator',
            password='12345'
        )
        Chat.objects.create(
            title='test-chat',
            creator=self.test_creator,
        )

    def test_get_chat(self):
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
                'creator': 6,
                'invited': [],
                'is_closed': False
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
        response = self.client.put(
            reverse('api:chat-detail', kwargs={'pk': self.test_chat_edit.pk}),
            data=json.dumps(self.edit_chat),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
