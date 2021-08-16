from django.contrib.auth import get_user_model
from django.db import models

from .choices import STATUS
from .fields import ContentTypeRestrictedFileField
from .managers import ChatManager, FileManager, MessageManager
from .mixins import TimestampMixin

User = get_user_model()


class Chat(TimestampMixin, models.Model):
    """
    Chat model
    """

    title = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator"
    )
    invited = models.ManyToManyField(User, related_name="invited")
    is_closed = models.BooleanField(default=False)

    objects = ChatManager()


class Message(TimestampMixin, models.Model):
    """
    Message model
    """

    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="sender",
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="recipient",
    )
    text = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=STATUS.choices,
        default=STATUS.NOT_VIEWED,
    )

    objects = MessageManager()


class File(TimestampMixin, models.Model):
    """
    File model
    """

    document = ContentTypeRestrictedFileField(
        blank=False,
        upload_to="file/",
        content_types=("activate"),
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    objects = FileManager()
