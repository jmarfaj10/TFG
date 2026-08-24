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
import numpy as np


DEPTH_VIS_MIN_M = 0.1
DEPTH_VIS_MAX_M = 10.0


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
        self.data_ws = None
        self.stream_ws = None
        self.camera_type = "rgb"

    def data_is_open(self) -> bool:
        return self.data_ws is not None and not self.data_ws.closed

    def encrypt(self, data: dict) -> str:
        json_data = json.dumps(data)
        return self.cipher.encrypt(json_data.encode('utf-8')).decode('utf-8')

    def decrypt(self, text: str) -> dict:
        raw_bytes = self.cipher.decrypt(text.encode('utf-8'))
        return json.loads(raw_bytes.decode('utf-8'))
    

class RobotWebSocket(Node):

    def __init__(self, host="localhost"):
        super().__init__('robotWebSocket')
        from rclpy.parameter import Parameter
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.host = host
        self.sessions = []

        self.privateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.privateKey.public_key()
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        import os
        # Obtenemos la ruta real del script actual (resolviendo posibles enlaces simbólicos de ROS)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Retrocedemos dos carpetas (robotWebSocket/robotWebSocket) hasta llegar a src/ y buscamos config.yaml
        config_path = os.path.abspath(os.path.join(script_dir, "..", "..", "config.yaml"))
        with open(config_path, "r", encoding="utf-8") as f:
            datos = yaml.safe_load(f)

        self.user = datos["user"]
        self.password = datos["password"]
        self.authport = datos["auth-port"]
        self.dataport = datos["data-port"]
        self.streamport = datos["stream-port"]
        self.ip = datos["ip"]

        self.data_clients = set()
        self.stream_clients = set()

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
        # El URDF del robot publica algunos frames con '/' inicial ('/base_link'), que tf2
        # descarta por ilegales, así que 'base_link' puede no existir en el árbol. Se usa el
        # primer candidato que sí esté disponible ('base_footprint' es la raíz que publica odom).
        self.robot_frame_candidates = ["base_link", "base_footprint"]
        self.robot_frame = None

        # Final
        self.current_final = None

        # Goal
        self.current_goal = None  

        # Cam
        self.bridge = cv_bridge.CvBridge()
        self.sub_cam = self.create_subscription(ComboImage, robotCoummunication.IMG_CHANNEL, self.get_camera, 10)
        self.latest_image = {"rgb": None, "depth": None}


    def _on_vlm_response(self, msg: String):
        try:
            payload = json.loads(msg.data)
            tipo, texto = payload.get("type", "vlm_response"), payload.get("data", "")
        except (json.JSONDecodeError, TypeError):
            tipo, texto = "vlm_response", msg.data
        self._broadcast_data(Response("SUCCESS", data={"type": tipo, "data": texto}).to_dict())

    def _broadcast_data(self, data: dict):
        """Envia un paquete ya serializado a todos los clientes del socket DATA
        desde un callback de ROS (hilo distinto al del bucle asyncio)."""
        if self.loop is None:
            return
        for session in list(self.data_clients):
            if session.data_is_open():
                paquete = session.encrypt(data)
                self.loop.call_soon_threadsafe(
                    asyncio.create_task, session.data_ws.send(paquete)
                )

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

            msg = Response("SUCCESS")

            await websocket.send(json.dumps(msg.to_dict()))

            login_credentials_str = await websocket.recv()
            login_credentials = json.loads(login_credentials_str)
            credentials = json.loads(cipher.decrypt(login_credentials["login_data"].encode('utf-8')).decode('utf-8'))

            session = ClientSession(client_ip, cipher, websocket)
            
            if credentials.get("user") == self.user and credentials.get("password") == self.password:
                session.token = str(uuid.uuid4())
                self.sessions.append(session)
                self.get_logger().info(f"(IP: {session.ip}) User access OK")
                response = Response("SUCCESS", f"You have been successfully connected {session.ip}", f"{session.token}")
                await websocket.send(session.encrypt(response.to_dict()))

            else:
                self.get_logger().error(f"(IP: {session.ip}) User access FAILED")
                response_err = Response("ERROR", "Invalid Credentials")
                await websocket.send(session.encrypt(response_err.to_dict()))
                await websocket.close()
                return
        except Exception as e:
            self.get_logger().error(f"Connection error for IP: ({client_ip}): {e}")

    async def get_session_from_encrypted_message(self, message: str):
        for s in self.sessions:
            try:
                decrypted_bytes = s.cipher.decrypt(message.encode('utf-8'))
                request = json.loads(decrypted_bytes.decode('utf-8'))
                if request.get("token") == s.token:
                    return s, request
            except Exception:
                continue
        return None, None
    
    # DATA WEBSOCKET
    async def data_handle(self, websocket):
        try:
            message = await websocket.recv()
            session, request = await self.get_session_from_encrypted_message(message)

            if session is not None:
                session.data_ws = websocket
                self.data_clients.add(session)
            else:
                await websocket.close(code=1008, reason="Invalid encrypted token")
                return

            async for message in websocket:
                try:
                    request = session.decrypt(message)
                except Exception:
                    await websocket.send(session.encrypt(Response("ERROR", "Invalid encryption or format").to_dict()))
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
                    await websocket.send(session.encrypt(Response("ERROR", "Not valid action").to_dict()))
                    continue

                match action_parts[0]:
                    case "vlm_request":
                        response = await self.vlm_request(params)
                    case _:
                        response = Response("ERROR", f"Unknown action '{action_parts[0]}'")

                if response:
                    await websocket.send(session.encrypt(response.to_dict()))
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.get_logger().error(f"Error in data_handle: {e}")
        finally:
            if 'session' in locals() and session in self.data_clients:
                session.data_ws = None
                self.data_clients.remove(session)

    async def vlm_request(self, params):                                                                                                                                                   
        prompt_text = params.get("prompt")
        
        if not prompt_text:   
            return Response("ERROR", "Atribute 'prompt' required for this action")

        msg = String()
        msg.data = prompt_text
        self.pub_usercomm.publish(msg)
        self.get_logger().info(f"[Server] Request was sent to VLM Node: '{prompt_text}'")

        return None

    def _resolve_robot_frame(self):
        for frame in self.robot_frame_candidates:
            if self.tf_buffer.can_transform(self.map_frame, frame, Time()):
                if self.robot_frame != frame:
                    self.robot_frame = frame
                    self.get_logger().info(f"TF: usando '{frame}' como frame del robot")
                return frame
        return None

    async def push_position_loop(self):
        while True:
            try:
                robot_frame = self._resolve_robot_frame()
                if robot_frame is not None:
                    t = self.tf_buffer.lookup_transform(
                        self.map_frame,
                        robot_frame,
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
                    
                    response = Response("SUCCESS", data={"type": "position", "data": pose_data})

                    for session in list(self.data_clients):
                        if session.data_is_open():
                            paquete = session.encrypt(response.to_dict())
                            await session.data_ws.send(paquete)
            except Exception as e:
                error_msg = str(e)
                if "extrapolation" not in error_msg.lower():
                    self.get_logger().error(f"TF Error: {error_msg}")
                
            await asyncio.sleep(0.1)

    def _goal(self, msg):
        self.current_goal = json.loads(msg.data)
        data = Response("SUCCESS", data={"type": "goal", "data": self.current_goal}).to_dict()
        self._broadcast_data(data)

    def _final(self, msg):
        self.current_final = json.loads(msg.data)
        data = Response("SUCCESS", data={"type": "final", "data": self.current_final}).to_dict()
        self._broadcast_data(data)

    # STREAM WEBSOCKET
    async def stream_handle(self, websocket):
        # Una tarea de streaming por cámara ('rgb'/'depth'): el cliente puede pedir ambas.
        streaming_tasks = {}
        try:
            message = await websocket.recv()
            session, request = await self.get_session_from_encrypted_message(message)

            if session is not None:
                session.stream_ws = websocket
                self.stream_clients.add(session)
            else:
                await websocket.close(code=1008, reason="Invalid encrypted token")
                return

            async for message in websocket:
                try:
                    request = session.decrypt(message)
                except Exception:
                    await websocket.send(session.encrypt(Response("ERROR", "Invalid encryption or format").to_dict()))
                    continue
                
                action_str = request.get("action", "")
                action_parts = [x for x in action_str.split("/") if x]

                if not action_parts:
                    await websocket.send(session.encrypt(Response("ERROR", "Not valid action").to_dict()))
                    continue

                match action_parts[0]:
                    case "camera":
                        if len(action_parts) > 1 and action_parts[1] in ["rgb", "depth"]:
                            camera_type = action_parts[1]
                            task = streaming_tasks.get(camera_type)
                            if task is None or task.done():
                                streaming_tasks[camera_type] = asyncio.create_task(
                                    self._camera_loop(session, camera_type)
                                )
                        else:
                            await websocket.send(session.encrypt(Response("ERROR", "Command not found").to_dict()))
                    case _:
                        await websocket.send(session.encrypt(Response("ERROR", f"Command '{action_parts[0]}' not found").to_dict()))

        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.get_logger().error(f"Error in stream_handle: {e}")
        finally:
            for task in streaming_tasks.values():
                task.cancel()
            if 'session' in locals() and session in self.stream_clients:
                session.stream_ws = None
                self.stream_clients.remove(session)

    async def _camera_loop(self, session, camera_type):
        try:
            # El socket de auth ya está cerrado en este punto: hay que emitir por el de streaming.
            while session.stream_ws is not None and not session.stream_ws.closed:
                img = self.latest_image.get(camera_type)
                if img is not None:
                    response = Response("SUCCESS", data={"type": f"camera_{camera_type}", "data": img})
                else:
                    response = Response("ERROR", "No image")
                await session.stream_ws.send(session.encrypt(response.to_dict()))
                await asyncio.sleep(1 / 30)
        except (asyncio.CancelledError, websockets.exceptions.ConnectionClosed):
            pass
    
    def depth_to_color(self, depth_msg):
        depth_m = np.array(self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding='passthrough'),
                           dtype=np.float32, copy=True)
        if depth_msg.encoding in ("16UC1", "mono16"):
            depth_m /= 1000.0

        valid = np.isfinite(depth_m) & (depth_m >= DEPTH_VIS_MIN_M)
        depth_u8 = np.zeros(depth_m.shape, dtype=np.uint8)
        scaled = (depth_m[valid] - DEPTH_VIS_MIN_M) / (DEPTH_VIS_MAX_M - DEPTH_VIS_MIN_M)
        depth_u8[valid] = (np.clip(scaled, 0.0, 1.0) * 255).astype(np.uint8)

        colored = cv2.applyColorMap(depth_u8, cv2.COLORMAP_TURBO)
        colored[~valid] = (0, 0, 0)
        return colored

    def get_camera(self, combo):
        try:
            cv_img_rgb = self.bridge.imgmsg_to_cv2(combo.img_rgb, desired_encoding='bgr8')
            success_rgb, encoded_image_rgb = cv2.imencode('.jpg', cv_img_rgb)

            cv_img_depth_vis = self.depth_to_color(combo.img_depth)
            success_depth, encoded_image_depth = cv2.imencode('.jpg', cv_img_depth_vis)

            if success_rgb and success_depth:
                self.latest_image["rgb"] = base64.b64encode(encoded_image_rgb).decode('utf-8')
                self.latest_image["depth"] = base64.b64encode(encoded_image_depth).decode('utf-8')
        except Exception as e:
            self.get_logger().error(f"Error procesando imagen de cámara: {e}")


async def main_async(node):                                              
    node.loop = asyncio.get_running_loop()
    
    asyncio.create_task(node.push_position_loop())

    server_auth = await serve(node.auth, node.ip, node.authport)
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
