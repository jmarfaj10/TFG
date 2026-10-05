import os
import yaml

_BASE = os.path.dirname(os.path.abspath(__file__))
try:
    from ament_index_python.packages import get_package_share_directory
    _TOPICS = os.path.join(get_package_share_directory("VLMProcessing"), "config.yaml")
except Exception:
    _TOPICS = os.path.join(_BASE, "..", "..", "config.yaml")
with open(_TOPICS) as f:
    datos = yaml.safe_load(f)
# Topics de cámara del robot (TIAGo). VLMProcessing los captura.
RGB_TOPIC = datos["rgb_cam_topic"]
DEPTH_TOPIC = datos["depth_cam_topic"]

API_URL = datos["api_url"]
MODEL_NAME = datos["model_name"]

COMM_CHANNEL_VLM = "comm_channel_vlm"

GOAL_CHANNEL_VLM = "goal_channel_vlm"

RESPONSE_CHANNEL_VLM = "response_channel_vlm"

VLM_COORD_SCALE = 1000

DEPTH_OPTICAL_FRAME = "camera_rgb_optical_frame"

STANDOFF_M = 1.2

BBOX_OUTPUT = "/root/tiago_public_ws/src/mis_nodos_tiago/vlm_bbox.jpg"

MAP_FRAME = "map"
ROBOT_FRAME = "base_link"
