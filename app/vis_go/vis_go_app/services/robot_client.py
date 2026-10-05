import contextvars
import asyncio
from websockets.asyncio.client import connect
import json
from cryptography.hazmat.primitives.asymmetric import padding                                                                                                                                            
from cryptography.hazmat.primitives import hashes                                                                                                                                                        
from cryptography.hazmat.primitives import serialization                                                                                                                                                 
from cryptography.fernet import Fernet
from channels.layers import get_channel_layer
from django.conf import settings
from datetime import timedelta
from vis_go_app.services import database_service
from vis_go_app.models import Mission
from channels.db import database_sync_to_async

class Response:
    def __init__(self, status, message=None, data=None, code=None):
        self.status = status
        self.message = message
        self.data = data
        self.code = code

    def to_dict(self):
        res = {"status": self.status}
        if self.message:
            res["message"] = self.message
        if self.data:
            res["data"] = self.data
        if self.code:
            res["code"] = self.code
        return res


USER_ERRORS = {
    "connection_refused": (
        "Could not reach the robot. Check that it is powered on and "
        "reachable on the network."
    ),
    "handshake_failed": "The robot did not complete the security key exchange.",
    "auth_failed": "The robot rejected the access credentials.",
    "data_ports_failed": (
        "Authenticated with the robot, but the data and video channels "
        "could not be opened."
    ),
    "no_connection": "There is no active connection to the robot.",
    "robot_lost": "The connection to the robot has been lost.",
}
UNKNOWN_ERROR = "Unknown error while connecting to the robot."


def error_response(code, detail=None):
    if detail:
        print(f"[robot_client] {code}: {detail}")
    return json.dumps(
        Response("ERROR", USER_ERRORS.get(code, UNKNOWN_ERROR), code=code).to_dict()
    )

class ServerSession:
    def __init__(self, ip: str, cipher: Fernet, websocket, user_id):
        self.ip = ip
        self.cipher = cipher
        self.websocket = websocket
        self.token = None
        self.user_id = user_id

    def encrypt(self, data: dict) -> str:
        json_data = json.dumps(data)
        return self.cipher.encrypt(json_data.encode('utf-8')).decode('utf-8')
    
    def decrypt(self, text: str) -> dict:
        raw_bytes = self.cipher.decrypt(text.encode('utf-8'))
        return json.loads(raw_bytes.decode('utf-8'))

class RobotClientManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RobotClientManager, cls).__new__(cls)
            cls._instance.session = None
            cls._instance.ws_data = None
            cls._instance.ws_stream = None
        return cls._instance

    async def connect_ws(self, user, password, user_id, user_ip):
        if self.session and self.ws_data and self.ws_stream:
            return json.dumps(Response("SUCCESS", "Connection established", self.session.token).to_dict())

        url_auth = f"ws://{settings.IP}:{settings.WS_AUTH_PORT}"
        data_port = getattr(settings, 'DATA_PORT', settings.WS_DATA_PORT)
        stream_port = getattr(settings, 'STREAMING_PORT', settings.WS_STREAMING_PORT)
        url_data = f"ws://{settings.IP}:{data_port}"
        url_stream = f"ws://{settings.IP}:{stream_port}"
        
        try:
            ws_auth = await connect(url_auth)
        except Exception as e:
            return error_response("connection_refused", e)
        
        msg = json.loads(await ws_auth.recv())
        if not msg:
            return error_response("handshake_failed", "empty init handshake")
            
        public_key = msg.get("rsa_public_key")
        if public_key is None:
            return error_response("handshake_failed", "missing rsa_public_key")

        public_key = serialization.load_pem_public_key(public_key.encode('utf-8'))

        fernet_key = Fernet.generate_key()
        cipher = Fernet(fernet_key)

        self.session = ServerSession(user_ip, cipher, ws_auth, user_id)

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
            return error_response("handshake_failed", "no OK received for the Fernet key")

        login_msg = {
            "login_data": login_data
        }

        await ws_auth.send(json.dumps(login_msg))
        
        msg = self.session.decrypt(await ws_auth.recv())
        await ws_auth.close()

        if not msg:
            return error_response("auth_failed", "empty login response")
        
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
                
                asyncio.create_task(self._background_listener(self.ws_data, "data_group"), context=contextvars.Context())
                asyncio.create_task(self._background_listener(self.ws_stream, "image_group"), context=contextvars.Context())
                
                return json.dumps(Response("SUCCESS", msg.get("message"), self.session.token).to_dict())
            except Exception as e:
                return error_response("data_ports_failed", e)
        else:
            return error_response("auth_failed", msg.get("message", "no message from server"))

    async def send_command(self, action: str, data: dict = None):
        if not self.ws_data or not self.session:
            return error_response("no_connection")
            
        # El servidor lee los argumentos de la clave 'params', no de la raíz del payload.
        payload = {"action": action}
        if data:
            payload["params"] = data


        await self.ws_data.send(self.session.encrypt(payload))
        return json.dumps(Response("SUCCESS", "Command sent").to_dict())

    async def _background_listener(self, websocket, group_name):
        channel_layer = get_channel_layer()
        session = self.session

        last_final = None
        last_vlm_request = None
        last_goal = None

        while True:
            try:
                msg = await websocket.recv()
                data = session.decrypt(msg)
                if data["status"]=="SUCCESS" and group_name == "data_group":
                    response_data = data["data"]
                    create = False
                    match(response_data.get("type")):
                        case "goal":
                            last_goal = response_data.get("data")
                            pass
                        case "vlm_response":
                            last_vlm_request = response_data.get("data")
                            pass
                        case "final":
                            create = True
                            last_final = response_data.get("data")
                            pass 
                    if create:
                        try:
                            payload = format_data(self.session.user_id, self.session.ip, last_final, last_vlm_request, last_goal)
                            await database_sync_to_async(database_service.create_log)(payload)
                        except Exception as e:
                            print(f"[robot_client] create_log failed: {e}")
                        finally:
                            last_final = last_vlm_request = last_goal = None

                if channel_layer:
                    await channel_layer.group_send(
                        group_name,
                        {"type": "notify", "data": data}
                    )
            except Exception as e:
                print(f"Listener {group_name} disconnected: {e}")

                was_connected = self.session is not None
                self.session = None
                self.ws_data = None
                self.ws_stream = None

                if was_connected and channel_layer:
                    await channel_layer.group_send(
                        "data_group",
                        {
                            "type": "robot_status",
                            "connected": False,
                            "message": USER_ERRORS["robot_lost"],
                        },
                    )
                break

robot_client = RobotClientManager()

def format_data(user_id, ip, last_final, last_vlm_request, last_goal):
    prompt_data= {}
    goal_data= {}
    mission_data= {}
    log_data= {"user_id": user_id, "ip": ip}

    #GOAL
    if last_goal:
        goal_pose= last_goal.get("goal_pose", None)
        goal_data["x"] = goal_pose.get("x", None)
        goal_data["y"] = goal_pose.get("y", None)
        goal_data["z"] = goal_pose.get("z", None)
    else:
        goal_data = None

    #PROMPT
    if last_vlm_request:
        prompt_data["prompt"] = last_vlm_request
        if last_goal:
            prompt_data["bbox"] = last_goal.get("bbox_image", None)
            prompt_data["object"] = last_goal.get("target", None)
        else:
            prompt_data["bbox"] = None
            prompt_data["object"] = ""
    else:
        prompt_data = None

    #MISSION
    if last_final:
        match last_final.get("state"):
            case Mission.State.REACHED:
                mission_data["state"] = Mission.State.REACHED
                pass
            case Mission.State.NOT_REACHED:
                mission_data["state"] = Mission.State.NOT_REACHED
                pass
            case Mission.State.REJECTED:
                mission_data["state"] = Mission.State.REJECTED
                pass
            case _:
                mission_data["state"] = Mission.State.REJECTED
                pass

        mission_data["distance"] = last_final.get("distance", None)

        if last_final.get("time", None):
            mission_data["time"] = timedelta(milliseconds=(last_final.get("time", None)))
        else:
            mission_data["time"] = None
        final_pose = last_final.get("final_pose") or [None, None, None]
        mission_data["x"] = final_pose[0]
        mission_data["y"] = final_pose[1]
        mission_data["z"] = final_pose[2]

    return {"log_data": log_data, "goal_data": goal_data, "mission_data": mission_data, "prompt_data": prompt_data}
    

    

