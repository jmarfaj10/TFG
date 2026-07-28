import asyncio
from websockets.server import serve
import websockets
import cv_bridge
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
import robotCommunication.constants as robotCoummunication
from userCommunication.userCommunication import String
import threading
from tf2_ros import Buffer, TransformListener
from rclpy.time import Time 
from interfaces.msg import ComboImage



class Response:
    def __init__(self, status, message):
        self.status = status
        self.message = message
class ClientSession:
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
    
class RobotWebSocket(Node):

    def __init__(self, host="localhost", authport="8764", dataport="8765", streamport="8766"):
        super().__init__('robotWebSocket')
        self.host = host
        self.authport = authport
        self.dataport = dataport
        self.streamport = streamport
        self.sessions = {}


        self.privateKey = rsa.generate_private_key()
        self.public_key = self.privateKey.public_key
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

        with open("config.yaml", "r", encoding="utf-8") as f:
            datos = yaml.safe_load(f)

        self.user = datos["user"]
        self.password = datos["password"]

        #ROS CHANNELS
        self.pub_usercomm = self.create_publisher(String, userCommunication.USER_CHANNEL_COMM, 10)
        self.sub_vlm_resp = self.create_subscription(String, userCommunication.RESPONSE_CHANNEL_VLM, self._on_vlm_response, 10) 

        # Cola/Futuros de peticiones VLM pendientes          constants.IMG_CHANNEL, 10                                                                                                                                                                                    
        self.pending_vlm_requests = []                                                                                                                                                                                                           
        self.loop = None   

        self.tf_buffer = Buffer()                                                                                           
        self.tf_listener = TransformListener(self.tf_buffer, self)                                                          
        self.map_frame = "map"          # Frame global de navegación                                                        
        self.robot_frame = "base_link"   

        #Cam
        self.bridge = cv_bridge()
        self.sub_cam = self.create_subscription(ComboImage, robotCoummunication.IMG_CHANNEL,self.get_camera, 10)
        

    async def auth(self, websocket):
        try:
            client_ip = websocket.remote_address
            self.get_logger().info("Season requested from (IP): ", client_ip)
            session=None
            await websocket.send(json.dumps({
                "type": "init_handshake",
                "rsa_public_key": self.public_pem
                }))

            init_msg = await websocket.recv()
            payload = json.loads(init_msg)
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
            session = ClientSession(client_ip, cipher, websocket)
            if credentials["user"]!=None and credentials["user"] == self.user and credentials["password"]!=None and credentials["password"] == self.password:

                session.token = str(uuid.uuid4())
                self.sessions[websocket] = session

                self.get_logger().info(f"(IP: {session.ip})User access OK")

                response = session.encrypt({"status": "SUCCESS", "token": f"{session.token}","message": f"You has been sucessfully conected {session.ip}"})

                await websocket.send(response)

                async for message in websocket:
                    response = await self.route(message)
                    response = session.encrypt(response)
                    await websocket.send(response)


            else:
                self.get_logger().error(f"(IP: {session.ip})User access FAILED")

                response = session.encrypt(json.dumps({"status": "ERROR", "message": "Invalid Credentials"}).encode('utf-8')).decode('utf-8')
                await websocket.send(response)
                await websocket.close()
                return
        except Exception as e:
            self.get_logger().error(f"Conection error for IP: ({client_ip}): {e}")

    async def route(self, message):
        request = None
        response = None
        try:
            request = json.loads(message)
        except json.JSONDecodeError:
            response = Response("ERROR")
            response.message = "Request must be a JSON"
        action = request.get("action", "")
        action = [x for x in action.split('/') if x]

        port_endpoint = action[0]
        action.pop(0)

        if port_endpoint == "data":
            try:
                request["action"] = "/" + "/".join(action)
                async with websockets.connect(f"ws://127.0.0.1:{self.dataport}") as internal_ws:
                    await internal_ws.send(json.dumps(request))
                    internal_response_raw = await internal_ws.recv()
                    response = json.loads(internal_response_raw)

            except Exception as e:
                self.get_logger().error(f"Error comunicando con Puerto Data (8765): {e}")
                response = Response("ERROR")
                response.message = f"Fallo en el servicio interno de datos: {str(e)}"

            
        elif port_endpoint == "stream":
            
        else:
            response = Response("Error")
            response.message = "Invalid route"


        if request is None or response is None:
            response = Response("ERROR")
            response.message = "Empty Response"

        return response
    
    #DATA WEBSOCKET
    async def data_handle(self, websocket):
        try:                                                                                                        
            async for message in websocket:
                request = None
                request = json.loads(message)
                if request.get("token") not in [s.token for s in self.sessions.values()]:
                    response = Response("ERROR")
                    response.message = "Server cannot find 'token' attribute"
                    return await websocket.send(json.dumps(request))

                action = request.get("action")
                action = action.split("/")
                params = dict(request.get("params"))

                if action is None:
                    response = Response("ERROR")
                    response.message = "Not valid action"

                match action[0]:
                    case "position":
                        response = self.get_robot_pose()
                    case "vlm_request":
                        response = self.vlm_request(params)
        except json.JSONDecodeError:
            response = Response("ERROR", "Json format needed")

        except asyncio.TimeoutError:
            response = Response("ERROR", "Timeout error")

        except Exception as e:
            response = Response("ERROR", f"{e}")

        return response

    async def vlm_request(self, params):                                                                                                                                                   
            prompt_text = params.get("prompt")                                                                                                                                                         
            if not prompt_text:   
                response = Response("ERROR")
                response.message = "Atribute 'prompt' required for this action"                                                                                                                                                                      
                return response
            fut = self.loop.create_future()
            self.pending_vlm_requests.append(fut)

            msg = String()
            msg.data = prompt_text
            self.pub_usercomm.publish(msg)
            self.get_logger().info(f"[Server]Request was sent to VLM Node: '{prompt_text}'")

            try:
                vlm_response = await asyncio.wait_for(fut, timeout=60.0)
                response = Response("SUCCESS")
                response.response = vlm_response
                return response
            except asyncio.TimeoutError:
                if fut in self.pending_vlm_requests:
                    self.pending_vlm_requests.remove(fut)
                response = Response("ERROR")
                response.message = "Timeout exception"
                return response
            except Exception as e:
                response = Response("ERROR")
                response.message = f"Error processing request in VLM Node: {str(e)}"

    async def get_robot_pose(self):
        response = None
        try:                                                                                                            
            t = self.tf_buffer.lookup_transform(                                                                        
                self.map_frame,                                                                                         
                self.robot_frame,                                                                                       
                Time()                                                                                                  
            )                                                                                                           
            p = t.transform.translation                                                                                 
            r = t.transform.rotation
            response = Response("SUCCESS", {                                                                                                    
                "x": round(float(p.x), 3),                                                                              
                "y": round(float(p.y), 3),                                                                              
                "z": round(float(p.z), 3),                                                                              
                "qx": round(float(r.x), 4),                                                                             
                "qy": round(float(r.y), 4),                                                                             
                "qz": round(float(r.z), 4),                                                                             
                "qw": round(float(r.w), 4)
            })                                                                                 
            return response
        except Exception as e:
            self.get_logger().warn(f"No hay TF {self.map_frame}->{self.robot_frame}: {e}")
            response = Response("ERROR", "Cannot find robot pose")
            return None

    #STREAM WEBSOCKET
    async def stream_handle(self, websocket):
        try:                                                                                                        
            async for message in websocket:
                request = None
                request = json.loads(message)
                if request.get("token") not in [s.token for s in self.sessions.values()]:
                    response = Response("ERROR")
                    response.message = "Server cannot find 'token' attribute"
                    return await websocket.send(json.dumps(request))

                action = request.get("action")
                action = action.split("/")
                params = dict(request.get("params"))

                match action[0]:
                    case "camera":
                        response = self.get_robot_pose()

        except json.JSONDecodeError:
            response = Response("ERROR", "Json format needed")

        except asyncio.TimeoutError:
            response = Response("ERROR", "Timeout error")

        except Exception as e:
            response = Response("ERROR", f"{e}")

        return response

    async def get_camera(self, combo):


async def main_async(node):                                                                                                                                                                                                  
    node.loop = asyncio.get_running_loop()
        
    # Iniciar ambos servidores WebSocket                
    server_auth = await serve(node.auth, "0.0.0.0", node.authport)
    server_data = await serve(node.data_handle, node.host, node.dataport)
    server_stream = await serve(node.handle_stream_connection, node.host, node.streamport)

    node.get_logger().info(f"🚀 WebSocket AUTH (8764) iniciado en ws://0.0.0.0:{node.authport}")
    node.get_logger().info(f"🚀 WebSocket DATA (8765) iniciado en ws://{node.host}:{node.dataport}")
    node.get_logger().info(f"🚀 WebSocket STREAMING (8766) iniciado en ws://{node.host}:{node.streamport}")
        
    # Tarea asíncrona en segundo plano: Difusión continua de posición a 5 Hz
    asyncio.create_task(node.)
    asyncio.create_task(node.)

    await asyncio.gather(
        server_auth.wait_closed(),
        server_data.wait_closed(),
        server_stream.wait_closed()
    )
    

def main(args=None):
    rclpy.init(args=args)
    node = RobotWebSocket()

        # El spin de ROS 2 corre en un hilo secundario para no bloquear asyncio
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    try:
        asyncio.run(main_async(node))
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    
if __name__ == '__main__':
    main()


