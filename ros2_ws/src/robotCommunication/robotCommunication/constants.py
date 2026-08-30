import os
import yaml

_BASE = os.path.dirname(os.path.abspath(__file__))
try:
    from ament_index_python.packages import get_package_share_directory
    _TOPICS = os.path.join(get_package_share_directory("robotCommunication"), "config.yaml")
except Exception:
    _TOPICS = os.path.join(_BASE, "..", "..", "config.yaml")
with open(_TOPICS) as f:
    datos = yaml.safe_load(f)

RGB_TOPIC = datos["rgb_cam_topic"]
DEPTH_TOPIC = datos["depth_cam_topic"]
DEPTH_INFO_TOPIC = datos["depth_info_topic"]
RGB_INFO_TOPIC = datos["rgb_info_topic"]
IMG_CHANNEL = "img_channel"
USER_CHANNEL_COMM = "user_channel_comm"
RESPONSE_CHANNEL_VLM = "response_channel_vlm"
COMM_CHANNEL_VLM = "comm_channel_vlm"
GOAL_CHANNEL_VLM = "goal_channel_vlm"
GOAL_CHANEL_ACTION = "move"
FINAL_CHANNEL = "final_channel"
GOAL_CHANNEL = "goal_channel"

