import asyncio
from websockets.server import serve
import websockets
import cv_bridge
import rclpy
from rclpy.node import Node
from urllib.parse import parse_qs, urlparse
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import yaml
import uuid
from userCommunication.userCommunication import constants as userCommunication
from robotCommunication.robotCommunication import constants as robotCoummunication

from userCommunication.userCommunication import String
import threading
from tf2_ros import Buffer, TransformListener
from rclpy.time import Time 
from interfaces.msg import ComboImage
import base64                                                            
import cv2   


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


class ClientSession:
    def __init__(self, ip: str, cipher: Fernet, websocket):
        self.ip = ip
        self.cipher = cipher
        self.websocket = websocket
        self.ip = websocket.remote_address
        self.token = None

    def encrypt(self, data: dict) -> str:
        json_data = json.dumps(data)
        return self.cipher.encrypt(json_data.encode('utf-8')).decode('utf-8')

    def decrypt(self, text: str) -> dict:
        raw_bytes = self.cipher.decrypt(text.encode('utf-8'))
        return json.loads(raw_bytes.decode('utf-8'))
    

class RobotWebSocket(Node):

    def __init__(self, host="localhost"):
        super().__init__('robotWebSocket')
        self.host = host
        self.sessions = {}

        self.privateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.privateKey.public_key()
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        with open("config.yaml", "r", encoding="utf-8") as f:
            datos = yaml.safe_load(f)

        self.user = datos["user"]
        self.password = datos["password"]
        self.authport = datos["auth-port"]
        self.dataport = datos["data-port"]
        self.streamport = datos["stream-port"]

        # ROS CHANNELS
        self.pub_usercomm = self.create_publisher(String, userCommunication.USER_CHANNEL_COMM, 10)
        self.sub_vlm_resp = self.create_subscription(String, userCommunication.RESPONSE_CHANNEL_VLM, self._on_vlm_response, 10) 
        self.sub_final = self.create_subscription(String, robotCoummunication.FINAL_CHANNEL, self._final, 10)
        self.sub_goal = self.create_subscription(String, robotCoummunication.GOAL_CHANNEL, self._goal, 10)

        # Cola/Futuros de peticiones VLM pendientes
        self.pending_vlm_requests = []                                                                                                                                                                                                           
        self.loop = None   

        self.tf_buffer = Buffer()                                                                                           
        self.tf_listener = TransformListener(self.tf_buffer, self)                                                          
        self.map_frame = "map"          # Frame global de navegación                                                        
        self.robot_frame = "base_link" 

        # Final
        self.current_final = None

        # Goal
        self.current_goal = None  

        # Cam
        self.bridge = cv_bridge.CvBridge()
        self.sub_cam = self.create_subscription(ComboImage, robotCoummunication.IMG_CHANNEL, self.get_camera, 10)
        self.latest_image = {"rgb": None, "depth": None}


    def _on_vlm_response(self, msg: String):
        if self.pending_vlm_requests:
            fut = self.pending_vlm_requests.pop(0)
            if not fut.done():
                self.loop.call_soon_threadsafe(fut.set_result, msg.data)

    async def auth(self, websocket):
        try:
            client_ip = websocket.remote_address
            self.get_logger().info(f"Session requested from (IP): {client_ip}")
            session = None
            await websocket.send(json.dumps({
                "type": "init_handshake",
                "rsa_public_key": self.public_pem
            }))

            init_msg = await websocket.recv()
            payload = json.loads(init_msg)
            fernet_key_bytes = self.privateKey.decrypt(
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
            
            if credentials.get("user") == self.user and credentials.get("password") == self.password:
                session.token = str(uuid.uuid4())
                self.sessions[websocket] = session
                self.get_logger().info(f"(IP: {session.ip}) User access OK")

                response_ok = {"status": "SUCCESS", "token": f"{session.token}", "message": f"You have been successfully connected {session.ip}"}
                await websocket.send(session.encrypt(response_ok))

                async for message in websocket:
                    # Desencriptar el mensaje entrante
                    decrypted_request = session.decrypt(message)
                    # Procesar la ruta
                    response_dict = await self.route(decrypted_request)
                    # Encriptar la respuesta y enviar
                    encrypted_response = session.encrypt(response_dict)
                    await websocket.send(encrypted_response)
            else:
                self.get_logger().error(f"(IP: {session.ip}) User access FAILED")
                response_err = {"status": "ERROR", "message": "Invalid Credentials"}
                await websocket.send(session.encrypt(response_err))
                await websocket.close()
                return
        except Exception as e:
            self.get_logger().error(f"Connection error for IP: ({client_ip}): {e}")

    async def route(self, request):
        if not isinstance(request, dict):
            # En caso de que se pase un string desencriptado en vez del dict
            if isinstance(request, str):
                try:
                    request = json.loads(request)
                except json.JSONDecodeError:
                    return Response("ERROR", "Request must be a JSON").to_dict()
            else:
                return Response("ERROR", "Request must be a JSON").to_dict()
                
        action = request.get("action", "")
        action_parts = [x for x in action.split('/') if x]

        if not action_parts:
            return Response("ERROR", "Empty route action").to_dict()

        port_endpoint = action_parts[0]
        action_parts.pop(0)

        if port_endpoint == "data":
            try:
                request["action"] = "/" + "/".join(action_parts)

                async with websockets.connect(f"ws://127.0.0.1:{self.dataport}") as internal_ws:
                    await internal_ws.send(json.dumps(request))
                    internal_response_raw = await internal_ws.recv()
                    return json.loads(internal_response_raw)
            except Exception as e:
                self.get_logger().error(f"Error comunicando con Puerto Data (8765): {e}")
                return Response("ERROR", f"Fallo en el servicio interno de datos: {str(e)}").to_dict()
            
        elif port_endpoint == "stream":
            try:
                request["action"] = "/" + "/".join(action_parts)
                async with websockets.connect(f"ws://127.0.0.1:{self.streamport}") as internal_ws:
                    await internal_ws.send(json.dumps(request))
                    internal_response_raw = await internal_ws.recv()
                    return json.loads(internal_response_raw)
            except Exception as e:
                self.get_logger().error(f"Error comunicando con Puerto Stream (8766): {e}")
                return Response("ERROR", f"Fallo en el servicio interno de streaming: {str(e)}").to_dict()
        else:
            return Response("ERROR", "Invalid route").to_dict()

    
    # DATA WEBSOCKET
    async def data_handle(self, websocket):
        try:                                                                                                        
            async for message in websocket:
                try:
                    request = json.loads(message)
                except json.JSONDecodeError:
                    response = Response("ERROR", "Json format needed")
                    await websocket.send(json.dumps(response.to_dict()))
                    continue

                if request.get("token") not in [s.token for s in self.sessions.values()]:
                    response = Response("ERROR", "Server cannot find 'token' attribute")
                    await websocket.send(json.dumps(response.to_dict()))
                    continue

                action = request.get("action", "")
                action_parts = [x for x in action.split("/") if x]
                params = request.get("params", {})
                if isinstance(params, str):
                    try:
                        params = json.loads(params)
                    except Exception:
                        params = {}

                if not action_parts:
                    response = Response("ERROR", "Not valid action")
                    await websocket.send(json.dumps(response.to_dict()))
                    continue

                match action_parts[0]:
                    case "position":
                        response = await self.get_robot_pose()
                    case "vlm_request":
                        response = await self.vlm_request(params)
                    case "goal":
                        if self.current_goal is not None:
                            response = Response("SUCCESS", data=self.current_goal)
                        else:
                            response = Response("ERROR", "There's no goal assigned - first prompt something")
                    case "final":
                        if self.current_final is not None:
                            response = Response("SUCCESS", data=self.current_final)
                        else:
                            response = Response("ERROR", "There's no final assigned - first prompt something")
                    case "help":
                        response = await self.help()
                    case _:
                        response = Response("ERROR", f"Unknown action '{action_parts[0]}'")

                await websocket.send(json.dumps(response.to_dict()))

        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.get_logger().error(f"Error in data_handle: {e}")

    async def vlm_request(self, params):                                                                                                                                                   
        prompt_text = params.get("prompt")                                                                                                                                                         
        if not prompt_text:   
            return Response("ERROR", "Atribute 'prompt' required for this action")

        fut = self.loop.create_future()
        self.pending_vlm_requests.append(fut)

        msg = String()
        msg.data = prompt_text
        self.pub_usercomm.publish(msg)
        self.get_logger().info(f"[Server] Request was sent to VLM Node: '{prompt_text}'")

        try:
            vlm_response = await asyncio.wait_for(fut, timeout=60.0)
            return Response("SUCCESS", data=vlm_response)
        except asyncio.TimeoutError:
            if fut in self.pending_vlm_requests:
                self.pending_vlm_requests.remove(fut)
            return Response("ERROR", "Timeout exception waiting for VLM")
        except Exception as e:
            if fut in self.pending_vlm_requests:
                self.pending_vlm_requests.remove(fut)
            return Response("ERROR", f"Error processing request in VLM Node: {str(e)}")

    async def get_robot_pose(self):
        try:                                                                                                            
            t = self.tf_buffer.lookup_transform(                                                                        
                self.map_frame,                                                                                         
                self.robot_frame,                                                                                       
                Time()                                                                                                  
            )                                                                                                           
            p = t.transform.translation                                                                                 
            r = t.transform.rotation
            pose_data = {                                                                                                    
                "x": round(float(p.x), 3),                                                                              
                "y": round(float(p.y), 3),                                                                              
                "z": round(float(p.z), 3),                                                                              
                "qx": round(float(r.x), 4),                                                                             
                "qy": round(float(r.y), 4),                                                                             
                "qz": round(float(r.z), 4),                                                                             
                "qw": round(float(r.w), 4)
            }
            return Response("SUCCESS", data=pose_data)
        except Exception as e:
            self.get_logger().warn(f"No hay TF {self.map_frame}->{self.robot_frame}: {e}")
            return Response("ERROR", "Cannot find robot pose")

    def _goal(self, msg):
        self.current_goal = json.loads(msg.data)

    def _final(self, msg):
        self.current_final = json.loads(msg.data)

    async def help(self):
        message = (
            "COMMAND LIST\n"
            "------------\n"
            "/data/position - returns the robot position\n"
            "/data/vlm_request - expects a prompt and returns a response from VLM\n"
            "/data/goal - returns the goal of the tarjet (None if there's no tarjet)\n"
            "/data/final - returns essential data when the move action finished"
        )
        return Response("SUCCESS", message)

    # STREAM WEBSOCKET
    async def stream_handle(self, websocket):
        try:                                                                                                        
            async for message in websocket:
                try:
                    request = json.loads(message)
                except json.JSONDecodeError:
                    response = Response("ERROR", "Json format needed")
                    await websocket.send(json.dumps(response.to_dict()))
                    continue
                
                if request.get("token") not in [s.token for s in self.sessions.values()]:
                    response = Response("ERROR", "Server cannot find 'token' attribute")
                    await websocket.send(json.dumps(response.to_dict()))
                    continue
                
                action_str = request.get("action", "")
                action_parts = [x for x in action_str.split("/") if x]

                if not action_parts:
                    response = Response("ERROR", "Not valid action")
                    await websocket.send(json.dumps(response.to_dict()))
                    continue

                match action_parts[0]:
                    case "camera":
                        if len(action_parts) > 1 and action_parts[1] in ["rgb", "depth"]:
                            camera_type = action_parts[1]
                            while not websocket.closed:
                                if self.latest_image[camera_type] is not None:
                                    response = Response("SUCCESS", data=self.latest_image[camera_type])
                                else:
                                    response = Response("ERROR", "No image")
                                
                                await websocket.send(json.dumps(response.to_dict()))
                                await asyncio.sleep(1 / 30)
                        else:
                            response = Response("ERROR", "Command not found")
                            await websocket.send(json.dumps(response.to_dict()))
                    case _:
                        response = Response("ERROR", f"Command '{action_parts[0]}' not found")
                        await websocket.send(json.dumps(response.to_dict()))

        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.get_logger().error(f"Error in stream_handle: {e}")

    def get_camera(self, combo):
        try:
            cv_img_rgb = self.bridge.imgmsg_to_cv2(combo.img_rgb, desired_encoding='bgr8')
            cv_img_depth = self.bridge.imgmsg_to_cv2(combo.img_depth, desired_encoding='passthrough')
            cv_img_depth_norm = cv2.normalize(cv_img_depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            success_rgb, encoded_image_rgb = cv2.imencode('.jpg', cv_img_rgb)
            success_depth, encoded_image_depth = cv2.imencode('.jpg', cv_img_depth_norm)
            
            if success_rgb and success_depth:
                self.latest_image["rgb"] = base64.b64encode(encoded_image_rgb).decode('utf-8')
                self.latest_image["depth"] = base64.b64encode(encoded_image_depth).decode('utf-8')
        except Exception as e:
            self.get_logger().error(f"Error procesando imagen de cámara: {e}")


async def main_async(node):                                              
    node.loop = asyncio.get_running_loop()

    server_auth = await serve(node.auth, "0.0.0.0", node.authport)
    server_data = await serve(node.data_handle, node.host, node.dataport)
    server_stream = await serve(node.stream_handle, node.host, node.streamport)

    node.get_logger().info(f"🚀 WebSocket AUTH ({node.authport}) iniciado en ws://0.0.0.0:{node.authport}")
    node.get_logger().info(f"🚀 WebSocket DATA ({node.dataport}) iniciado en ws://{node.host}:{node.dataport}")
    node.get_logger().info(f"🚀 WebSocket STREAMING ({node.streamport}) iniciado en ws://{node.host}:{node.streamport}")

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
