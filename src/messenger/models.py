from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from .mixins import TimestampMixin, UUIDModel
from .choices import STATUS

User = get_user_model()


class Chat(UUIDModel, TimestampMixin, models.Model):
    """
    Chat model
    """
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    invited = models.ManyToManyField(User, related_name='invited')
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Message(UUIDModel, TimestampMixin, models.Model):
    """
    Message model
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.NOTVIEWED)


class File(UUIDModel, TimestampMixin, models.Model):
    """
    File model
    """
    document = models.FileField(blank=False, upload_to='file/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
