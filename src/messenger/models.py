from django.contrib.auth import get_user_model
from django.db import models

from .choices import STATUS
from .mixins import TimestampMixin, UUIDModel

User = get_user_model()


class Chat(UUIDModel, TimestampMixin, models.Model):
    """
    Chat model
    """

    title = models.CharField(max_length=50)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator"
    )
    invited = models.ManyToManyField(User, related_name="invited")
    is_closed = models.BooleanField(default=False)


class Message(UUIDModel, TimestampMixin, models.Model):
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
    message = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=STATUS.NOTVIEWED,  # pylint: disable=E1101
    )


class File(UUIDModel, TimestampMixin, models.Model):
    """
    File model
    """

    document = models.FileField(blank=False, upload_to="file/")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    class Meta:
        ordering = ("document",)
