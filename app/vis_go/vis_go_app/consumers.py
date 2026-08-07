from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RobotConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if not self.scope["session"].get("auth"):
            await self.close()
            return

        self.image_group = "image_group"
        self.data_group = "data_group"

        await self.channel_layer.group_add(
            self.image_group,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.data_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'image_group'):
            await self.channel_layer.group_discard(
                self.image_group,
                self.channel_name
            )
            await self.channel_layer.group_discard(
                self.data_group,
                self.channel_name
            )

    async def notify(self, event):
        data_recv = event['datos']
        await self.send(text_data=json.dumps({
            "data": data_recv
        }))