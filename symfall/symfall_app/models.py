from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):  # -> Create model USER
    bio = models.TextField(max_length=200, null=True, blank=True)  # -> User information or biography
    birthday = models.DateTimeField(null=True, blank=True)  # -> information about birthday


class Chat(models.Model):  # -> Create model Chat

    class Meta:
        db_table = 'Chat'
        verbose_name = 'Chat room'
        verbose_name_plural = 'Chat rooms'

    chat_name = models.TextField(max_length=50, null=True, blank=True)  # -> Chat name
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')  # -> Creator Chat room
    invited = models.ManyToManyField(User, related_name='invited')
    date_create = models.DateTimeField(auto_now=True)  # date to create chat room
    is_close_chat = models.BooleanField(default=False)  # Check on open chat room or close chat room


class Message(models.Model):  # -> Create model Message

    class Meta:
        db_table = 'Message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')  # -> Sender from User
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='recipient')  # -> Recipient to Chat
    message = models.TextField(max_length=2000)  # -> Message text
    message_status = models.BooleanField(default=False)  # -> Message status (read or not read)
    time_to_post = models.DateTimeField(auto_now_add=True)  # -> Message dispatch time


class File(models.Model):  # -> Create model File

    class Meta:
        db_table = 'File'
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    document = models.FileField(null=True, blank=True, upload_to='file/')  # -> Files and documents
    message_key = models.ForeignKey(Message, on_delete=models.CASCADE)  # -> binding with Message
