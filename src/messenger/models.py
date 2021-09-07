from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    TextField,
)

from .choices import STATUS
from .fields import ContentTypeRestrictedFileField
from .managers import ChatManager, FileManager, MessageManager
from .mixins import TimestampMixin

User = get_user_model()


class Chat(TimestampMixin, Model):
    """
    Chat model
    """

    title = CharField(max_length=50, unique=True)
    creator = ForeignKey(User, on_delete=CASCADE, related_name="creator")
    invited = ManyToManyField(User, related_name="invited")
    is_closed = BooleanField(default=False)

    objects = ChatManager()


class Message(TimestampMixin, Model):
    """
    Message model
    """

    sender = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="sender",
    )
    chat = ForeignKey(
        to=Chat,
        on_delete=CASCADE,
        related_name="recipient",
    )
    text = TextField()
    status = PositiveSmallIntegerField(
        choices=STATUS.choices,
        default=STATUS.NOT_VIEWED,
    )

    objects = MessageManager()


class File(TimestampMixin, Model):
    """
    File model
    """

    document = ContentTypeRestrictedFileField(
        upload_to="file/",
    )
    message = ForeignKey(Message, on_delete=CASCADE)

    objects = FileManager()
