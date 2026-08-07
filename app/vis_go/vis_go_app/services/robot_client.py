import yaml
import asyncio
from websockets.asyncio.client import connect
import base64
import json
from cryptography.hazmat.primitives.asymmetric import padding                                                                                                                                            
from cryptography.hazmat.primitives import hashes                                                                                                                                                        
from cryptography.hazmat.primitives import serialization                                                                                                                                                 
from cryptography.fernet import Fernet
from channels.layers import get_channel_layer
from django.conf import settings

class Response:
    def __init__(self, status, message=None, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        res = {"status": self.status}
        if self.message:
            res["message"] = self.message
        if self.data:
            res["data"] = self.data
        return res

class ServerSession:
    def __init__(self, ip: str, cipher: Fernet, websocket):
        self.ip = ip
        self.cipher = cipher
        self.websocket = websocket
        self.token = None

    def encrypt(self, data: dict) -> str:
        json_data = json.dumps(data)
        return self.cipher.encrypt(json_data.encode('utf-8')).decode('utf-8')
    
    def decrypt(self, text: str) -> dict:
        raw_bytes = self.cipher.decrypt(text.encode('utf-8'))
        return json.loads(raw_bytes.decode('utf-8'))

class RobotClientManager:
    """Singleton para mantener la conexión WebSocket activa a través de toda la app"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RobotClientManager, cls).__new__(cls)
            cls._instance.session = None
            cls._instance.websocket = None
        return cls._instance

    async def connect_ws(self, user, password):
        
        url = f"ws://{settings.IP}:{settings.WS_PORT}"
        response = None
        
        try:
            self.websocket = await connect(url)
        except Exception as e:
            response = Response("ERROR", f"Connection refused or failed")
            return json.dumps(response.to_dict())
        
        msg = json.loads(await self.websocket.recv())
        if not msg:
            response = Response("ERROR", "Init_handshake is None")
            return json.dumps(response.to_dict())
            
        public_key = None
        if msg.get("type") == "init_handshake":
            public_key = msg.get("rsa_public_key")

        if public_key is None:
            response = Response("ERROR", "Public key is None")
            return json.dumps(response.to_dict())

        public_key = serialization.load_pem_public_key(public_key.encode('utf-8'))

        fernet_key = Fernet.generate_key()
        cipher = Fernet(fernet_key)

        self.session = ServerSession(self.websocket.remote_address, cipher, self.websocket)

        login_data = self.session.encrypt({"user": user, "password": password})

        encrypted_fernet_key = public_key.encrypt(fernet_key, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))

        payload = {
            "fernet_key_encrypted": encrypted_fernet_key.hex(),
            "login_data_encrypted": login_data
        }

        await self.websocket.send(json.dumps(payload))

        msg = self.session.decrypt(await self.websocket.recv())

        if not msg:
            response = Response("ERROR", "Response data not found")
            return json.dumps(response.to_dict())
        
        if msg.get("status") == "ERROR":
            response = Response("ERROR", msg.get("message", "Error from server"))
            return json.dumps(response.to_dict())

        if msg.get("status") == "SUCCESS":
            self.session.token = msg.get("data")
            response = Response("SUCCESS", msg.get("message"), self.session.token)

            asyncio.create_task(self._background_listener())

        if not response:
            response = Response("ERROR", "Unknown error")

        return json.dumps(response.to_dict())

    async def send_command(self, action: str, data: dict = None):

        if not self.websocket or not self.session:
            return json.dumps(Response("ERROR", "No hay conexión activa con el robot").to_dict())
            
        payload = {"action": action}
        if data:
            payload.update(data)
            
        await self.websocket.send(self.session.encrypt(payload))
        response = self.session.decrypt(await self.websocket.recv())
        return json.dumps(response)

    async def _background_listener(self):
            channel_layer = get_channel_layer()

            while True:
                try:
                    msg = await self.websocket.recv()

                    data = self.session.decrypt(msg)

                    if channel_layer:
                        if data.get("type") == "camera_rgb" or data.get("type") == "camera_depth":
                            await channel_layer.group_send(
                                "image_group",
                                {"data": data}
                            )
                        else:
                            await channel_layer.group_send(
                                "data_group",
                                {"data": data}
                            )
                except Exception as e:
                    print(f"Desconexión del listener del robot: {e}")
                    self.websocket = None
                    break

robot_client = RobotClientManager()