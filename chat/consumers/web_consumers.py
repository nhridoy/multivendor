import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AsyncWebConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        key = self.scope['url_route']['kwargs']['key']
        self.group_name = key

        # Send message to room group
        # await self.channel_layer.group_add(
        #     self.group_name,
        #     str(self.channel_name)
        # )
        #
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "socket_connected",
                "data": "Connected...",

            },
        )

        await self.accept()
        # else:
        #     await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "recent_messages",
                "data": text_data,
            },
        )

    # Socket Connection message
    async def socket_connected(self, event):
        await self.send(
            text_data=json.dumps(
                {"data": event["data"]}
            )
        )

    #  sent message to the group
    async def recent_messages(self, event):
        await self.send(
            text_data=json.dumps(
                {"data": event["data"]}
            )
        )
