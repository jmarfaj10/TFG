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
            cls._instance.ws_data = None
            cls._instance.ws_stream = None
        return cls._instance

    async def connect_ws(self, user, password):
        if self.session and self.ws_data and self.ws_stream:
            return json.dumps(Response("SUCCESS", "Conexión establecida", self.session.token).to_dict())

        url_auth = f"ws://{settings.IP}:{settings.WS_AUTH_PORT}"
        data_port = getattr(settings, 'DATA_PORT', settings.WS_DATA_PORT)
        stream_port = getattr(settings, 'STREAMING_PORT', settings.WS_STREAMING_PORT)
        url_data = f"ws://{settings.IP}:{data_port}"
        url_stream = f"ws://{settings.IP}:{stream_port}"
        
        try:
            ws_auth = await connect(url_auth)
        except Exception as e:
            return json.dumps(Response("ERROR", "Connection refused or failed").to_dict())
        
        msg = json.loads(await ws_auth.recv())
        if not msg:
            return json.dumps(Response("ERROR", "Init_handshake is None").to_dict())
            
        public_key = msg.get("rsa_public_key")
        if public_key is None:
            return json.dumps(Response("ERROR", "Public key is None").to_dict())

        public_key = serialization.load_pem_public_key(public_key.encode('utf-8'))

        fernet_key = Fernet.generate_key()
        cipher = Fernet(fernet_key)

        self.session = ServerSession(ws_auth.remote_address, cipher, None)

        login_data = self.session.encrypt({"user": user, "password": password})
        encrypted_fernet_key = public_key.encrypt(fernet_key, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))

        payload = {
            "fernet_key_encrypted": encrypted_fernet_key.hex(),
        }

        await ws_auth.send(json.dumps(payload))

        msg_ok = json.loads(await ws_auth.recv())
        if msg_ok.get("status") != "SUCCESS":
            return json.dumps(Response("ERROR", "OK not received").to_dict())

        login_msg = {
            "login_data": login_data
        }

        await ws_auth.send(json.dumps(login_msg))
        
        msg = self.session.decrypt(await ws_auth.recv())
        await ws_auth.close()

        if not msg:
            return json.dumps(Response("ERROR", "Response data not found").to_dict())
        
        if msg.get("status") == "SUCCESS":
            self.session.token = msg.get("data")
            
            try:
                self.ws_data = await connect(url_data)
                self.ws_stream = await connect(url_stream)
                
                token_msg = self.session.encrypt({"token": self.session.token})
                await self.ws_data.send(token_msg)
                await self.ws_stream.send(token_msg)
                
                await self.ws_stream.send(self.session.encrypt({"action": "camera/rgb"}))
                await self.ws_stream.send(self.session.encrypt({"action": "camera/depth"}))
                
                asyncio.create_task(self._background_listener(self.ws_data, "data_group"))
                asyncio.create_task(self._background_listener(self.ws_stream, "image_group"))
                
                return json.dumps(Response("SUCCESS", msg.get("message"), self.session.token).to_dict())
            except Exception as e:
                return json.dumps(Response("ERROR", f"Error conectando a los puertos de datos: {e}").to_dict())
        else:
            return json.dumps(Response("ERROR", msg.get("message", "Error from server")).to_dict())

    async def send_command(self, action: str, data: dict = None):
        if not self.ws_data or not self.session:
            return json.dumps(Response("ERROR", "No hay conexión activa con el robot").to_dict())
            
        # El servidor lee los argumentos de la clave 'params', no de la raíz del payload.
        payload = {"action": action}
        if data:
            payload["params"] = data


        await self.ws_data.send(self.session.encrypt(payload))
        return json.dumps(Response("SUCCESS", "Comando enviado").to_dict())

    async def _background_listener(self, websocket, group_name):
        channel_layer = get_channel_layer()
        # Referencia local: si el otro listener cae y limpia self.session, este debe
        # seguir descifrando hasta que su propio socket se cierre (y no romper con NoneType).
        session = self.session

        while True:
            try:
                msg = await websocket.recv()
                data = session.decrypt(msg)

                if channel_layer:
                    await channel_layer.group_send(
                        group_name,
                        {"type": "notify", "data": data}
                    )
            except Exception as e:
                print(f"Desconexión del listener {group_name}: {e}")
                self.session = None
                self.ws_data = None
                self.ws_stream = None
                break

robot_client = RobotClientManager()