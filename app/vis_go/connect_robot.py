import yaml
from websockets import asyncio
import websockets

def connect(user, password):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    url_auth = f"ws//:{config["ip"]}:{config["ws_port"]}"

    websockets.connect.open_tcp_connection
