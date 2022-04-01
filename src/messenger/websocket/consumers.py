from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Chat consumer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = None

    async def connect(self):
        """
        Connect to room
        """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        await self.channel_layer.group_add(self.chat_id, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        """Leave the room

        Args:
            code: Code of disconnect
        """
        await self.channel_layer.group_discard(self.chat_id, self.channel_name)

    async def send_message(self, response):
        """Receive message from room group

        Args:
            response: Message from room group
        """
        await self.send_json(response)
