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

# ---------------------------------------------------------------------------
# Ground-truth de objetos en la simulación (para el logger de error del goal)
# ---------------------------------------------------------------------------
# La posición REAL de cada objeto se consulta a Gazebo por gz-transport con
# 'gz topic -e'. Sirve para comparar el goal estimado por el VLM contra la
# posición real del objeto en el mundo simulado.
GZ_POSE_TOPIC = "/world/default/pose/info"

# Reglas etiqueta_del_VLM -> modelos de gz. Se busca por subcadena en
# minúsculas; si una regla casa con varios modelos (p.ej. las 4 cajas) se usa
# el CENTROIDE del grupo como posición real del objeto.
GT_OBJETOS = [
    {"keywords": ["buzon", "buzón", "postbox", "mailbox", "mail box", "correos", "post box"],
     "modelos": ["postbox"]},
    {"keywords": ["persona", "person", "hombre", "man", "people", "gente", "human"],
     "modelos": ["person_standing"]},
]
