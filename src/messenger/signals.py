import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from messenger.models import File, Message


@receiver(post_save, sender=Message)
def send_message_to_ws(sender, instance, created, **kwargs):  # noqa
    """
    Send message data to the WebSockets
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(instance.chat.id),
        {
            "type": "send_json",
            "text": instance.text,
            "created": created,
            "id": instance.id,
        },
    )


@receiver(post_delete, sender=File)
def delete_physical_file(sender, instance, **kwargs):  # noqa
    """
    Delete physical file from File System
    """
    if instance.document and instance.document.path:
        os.remove(instance.document.path)
