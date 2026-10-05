from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .services.robot_client import robot_client

class RobotConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")

        if user is None or not user.is_authenticated:
            await self.accept()
            await self.close(code=4001)
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


        await self.send(text_data=json.dumps({
            "event": "connected",
            "user": user.get_username(),
            "robot_connected": robot_client.session is not None,
        }))

    async def disconnect(self, code):
        if hasattr(self, 'image_group'):
            await self.channel_layer.group_discard(
                self.image_group,
                self.channel_name
            )
            await self.channel_layer.group_discard(
                self.data_group,
                self.channel_name
            )

    async def robot_status(self, event):
        await self.send(text_data=json.dumps({
            "event": "robot_status",
            "robot_connected": event.get("connected", False),
            "message": event.get("message"),
        }))

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
            print(f"Error handling incoming message in the consumer: {e}")
