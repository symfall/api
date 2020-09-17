from django.db import models
from django.contrib.auth.models import AbstractUser
from .mixins import Timestamps


class User(Timestamps, AbstractUser):
    """
    User model
    """
    biography = models.TextField(max_length=200, null=True, blank=True)


class Chat(Timestamps, models.Model):
    """
    Chat model
    """
    chat_name = models.TextField(max_length=50, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    invited = models.ManyToManyField(User, related_name='invited')
    is_close_chat = models.BooleanField(default=False)


class Message(Timestamps, models.Model):
    """
    Message model
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField(max_length=2000)

    """
    Create choice message status
    """
    STATUS = (
        ('V', 'viewed'),
        ('N', 'not viewed')
    )

    status = models.CharField(max_length=1, choices=STATUS)


class File(Timestamps, models.Model):
    """
    File model
    """
    document = models.FileField(blank=False, upload_to='file/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
