from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class RobotConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        is_auth = await sync_to_async(self.scope["session"].get)("auth")
        if not is_auth:
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
        data_recv = event['data']
        await self.send(text_data=json.dumps({
            "data": data_recv
        }))

    async def receive(self, text_data):
        from .services.robot_client import robot_client
        try:
            data = json.loads(text_data)
            action = data.get("action")
            params = data.get("params", {})
            
            if action:
                await robot_client.send_command(action, params)
        except Exception as e:
            print(f"Error procesando mensaje entrante en el consumer: {e}")