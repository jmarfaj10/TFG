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
import urllib
import uuid
from userCommunication.userCommunication import constants as userCommunication
from userCommunication.userCommunication.userCommunication import String

class Response:
    def __init__(self, status):
        self.status = status
        
class ClientSeasson:
    def __init__(self, ip: str, cipher: Fernet, websocket):
        self.ip = ip
        self.cipher = cipher
        self.websocket = websocket
        self.ip = websocket.remote_address
        self.token = None
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
    

    async def data_handle(self, websocket):
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

                    session.token = str(uuid.uuid4())
                    self.data_sessions[websocket] = session

                    self.get_logger().info(f"(IP: {session.ip})User access OK")

                    response = session.encrypt({"status": "SUCCESS", "token": f"{session.token}","message": f"You has been sucessfully conected {session.ip}"})

                    await websocket.send(response)

                else:
                    self.get_logger().error(f"(IP: {session.ip})User access FAILED")

                    response = session.encrypt(json.dumps({"status": "ERROR", "message": "Invalid Credentials"}).encode('utf-8')).decode('utf-8')
                    await websocket.send(response)
                    await websocket.close()
                    return


                async for message in websocket:
                    message = session.decrypt(message)
                    request = json.load(message)
                    if request==None:
                        self.get_logger().error("La peticion no cumple el formato necesario")
                        return 

                    if request["token"] in [session["token"] for session in self.sessions]:
                        action = request["action"]
                        if action!=None:
                            match action:
                                case "robot_position":
                                    

            except Exception as e:
                self.get_logger().error(f"Conection error for IP: ({client_ip}): {e}")


    async def handle_data(self, params):
        action = params["action"]
        response = ""
        match action:
            case "vlm_request":
                response =self.vlm_request(params)


            case "vlm_response":
                  self.vlm_response(params)

        return response

            



    




    async def vlm_request(self, session, params):                                                                                                                                                   
            prompt_text = params.get("request")                                                                                                                                                         
            if not prompt_text:                                                                                                                                                                         
                return session.encrypt(                                                                                                                                                                 
                    {                                                                                                                                                                                   
                        "status": "ERROR",                                                                                                                                                              
                        "message": "La acción vlm_request requiere el atributo 'request'",                                                                                                              
                    }                                                                                                                                                                                   
                )                                                                                                                                                                                       
                                                                                                                                                                                                        
            # Verificar si el servicio ROS 2 está disponible                                                                                                                                            
            if not self.vlm_client.wait_for_service(timeout_sec=1.0):                                                                                                                                   
                self.get_logger().warn(                                                                                                                                                                 
                    "Servicio ROS 2 'vlm_service' no disponible"                                                                                                                                        
                )                                                                                                                                                                                       
                return session.encrypt(                                                                                                                                                                 
                    {                                                                                                                                                                                   
                        "status": "ERROR",                                                                                                                                                              
                        "message": "Servicio VLM en el robot no disponible",                                                                                                                            
                    }
                )
  
            # Preparar la petición para el servicio ROS 2
            srv_request = SetString.Request()
            srv_request.data = prompt_text
  
            try:
                # 1. Llamar al servicio ROS 2 de forma asíncrona
                ros_future = self.vlm_client.call_async(srv_request)
  
                # 2. Convertir el Future de ROS a un Future de asyncio y ESPERAR LA RESPUESTA
                # Esto pausa solo esta corrutina sin congelar el nodo ni el servidor WebSocket
                ros_response = await asyncio.wrap_future(ros_future)
  
                # 3. Formatear la respuesta devuelta por el nodo ROS 2 y encriptarla para el cliente
                return session.encrypt(
                    {
                        "status": "SUCCESS",
                        "success": ros_response.success,
                        "result": ros_response.message,
                    }
                )
  
            except Exception as e:
                self.get_logger().error(f"Error al llamar al servicio VLM: {e}")
                return session.encrypt(
                    {
                        "status": "ERROR",
                        "message": f"Fallo en el servicio ROS 2: {str(e)}",
                    }
                )
