import asyncio
from websockets.server import serve
import rclpy
from rclpy import Node
from urllib.parse import parse_qs, urlparse
import json
# 1. Para generar claves RSA (privada y pública)
from cryptography.hazmat.primitives.asymmetric import rsa
# 2. Para aplicar relleno (padding) y algoritmos de hash al encriptar/desencriptar
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
# 3. Para convertir la clave pública a formato texto (PEM) y viceversa
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import yaml


class ClientSeasson:
    def __init__(self, ip: str, cipher: Fernet, websocket):
        self.ip = ip
        self.cipher = cipher
        self.websocket = websocket
        self.ip = websocket.remote_address
    def encrypt(self, dict: dict) -> str:
        json = json.dumps(dict)
        return self.cipher.encrypt(json.encode('utf-8')).decode('utf-8')
    def decrypt(self, text: str) -> dict:
        bytes = self.cipher.decrypt(text.encode('utf-8'))
        return json.loads(bytes.decode('utf-8'))
    
class robotWebSocket(Node):

    def __init__(self, host="localhost", port="8765"):
        super.__init__('robotWebSocket')
        self.host = host
        self.port = port
        self.sessions = {}
        self.privateKey = rsa.generate_private_key()
        self.public_key = self.privateKey.public_key
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

        with open("archivo.yaml", "r", encoding="utf-8") as f:
            datos = yaml.safe_load(f)

        self.user = datos["user"]
        self.password = datos["password"]

    

    async def client_management(self, websocket):
            client_ip = websocket.remote_address
            self.get_logger().info("Season requested from (IP): ", client_ip)
            session=None
            try:
                await websocket.send(json.dumps({
                    "type": "init_handshake",
                    "rsa_public_key": self.public_pem
                    }))

                init_msg = await websocket.recv()
                payload = json.load(init_msg)
                fernet_key_bytes = self.private_key.decrypt(
                bytes.fromhex(payload["fernet_key_encrypted"]),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                    )
                )

                cipher = Fernet(fernet_key_bytes)

                credentials = json.loads(cipher.decrypt(payload["login_data_encrypted"].encode('utf-8')).decode('utf-8'))
                session = ClientSeasson(client_ip, cipher, websocket)
                if credentials["user"]!=None and credentials["user"] == self.user and credentials["password"]!=None and credentials["password"] == self.password:
                    
                    self.sessions[websocket] = session

                    self.get_logger().info(f"(IP: {session.ip})User access OK")

                    response = session.encrypt({"status": "SUCCESS", "message": f"You has been sucessfully conected {session.ip}"})

                    await websocket.send(response)

                else:
                    self.get_logger().error(f"(IP: {session.ip})User access FAILED")

                    response = session.encrypt(json.dumps({"status": "ERROR", "message": "Invalid Credentials"}).encode('utf-8')).decode('utf-8')
                    await websocket.send(response)
                    await websocket.close()
                    return

                tarea_envio = asyncio.create_task(bucle_envio_datos(websocket, usuario_autenticado))
                async for mensaje in :
                    print(f"📩 Mensaje recibido de {usuario_autenticado}: {mensaje}")
                    
                    # Si el cliente solicita salir explícitamente
                    if mensaje == "EXIT":
                        print(f"Usuario {usuario_autenticado} solicitó EXIT.")


            except Exception as e:
                self.get_logger().error(f"Conection error for IP: ({client_ip}): {e}")
            
    #websocket para video
    async with serve(client_management, "localhost", 8765) as server:
        await server.serve_forever()




