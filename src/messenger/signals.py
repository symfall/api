from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from messenger.models import Message


@receiver(post_save, sender=Message)
def send_message_to_ws(
    sender, instance, created, **kwargs  # pylint: disable=W0613
):
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
