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

# Servidor VLM (antes en .env)
API_URL = datos["api_url"]
MODEL_NAME = datos["model_name"]

# robotCommunication -> VLMProcessing (texto de la petición)
COMM_CHANNEL_VLM = "comm_channel_vlm"

# VLMProcessing -> robotCommunication (objetivo de movimiento)
GOAL_CHANNEL_VLM = "goal_channel_vlm"

# VLMProcessing -> userCommunication (respuesta en texto al usuario)
RESPONSE_CHANNEL_VLM = "response_channel_vlm"

# Escala de coordenadas que devuelve el VLM (Qwen-VL usa 0-1000 normalizado)
VLM_COORD_SCALE = 1000

# Frame ÓPTICO de la cámara de profundidad. El punto 3D se calcula con los
# intrínsecos de profundidad en convención óptica (z = hacia delante, x =
# derecha, y = abajo), así que hay que transformarlo a 'map' desde este frame.
# OJO: el header del mensaje de profundidad trae un frame NO-óptico
# ('camera_rgb_frame'), que mezclaría los ejes y colocaría la profundidad en la
# Z del mapa; por eso se fuerza aquí el frame óptico correcto.
DEPTH_OPTICAL_FRAME = "camera_depth_optical_frame"

# Distancia de aproximación (m). El goal NO se pone sobre el objeto (celda
# letal del costmap: Nav2 no puede planificar ahí y el robot no rodea), sino a
# esta distancia DELANTE del objeto, sobre el rayo robot->objeto, en espacio
# libre. Debe ser >= radio del robot + radio de inflación del costmap.
# TIAGo: radio ~0.3 m + inflación ~0.5 m -> 0.8 m es un punto de partida.
STANDOFF_M = 0.5

# Ruta donde guardar la imagen con la bbox dibujada.
# Está dentro de la carpeta montada (./tiago_nodes en el host) para poder verla.
BBOX_OUTPUT = "/root/tiago_public_ws/src/mis_nodos_tiago/vlm_bbox.jpg"

# ---------------------------------------------------------------------------
# Ground-truth de objetos (para el logger de error del VLM)
# ---------------------------------------------------------------------------
# El pose real de cada modelo se consulta a Gazebo por gz-transport. NO se usa
# el bridge a /world/default/pose/info porque el conversor Pose_V->TFMessage
# pierde los nombres de frame (llegan vacíos) y no se puede identificar el
# objeto. Con 'gz topic -e' los nombres sí vienen.
GZ_POSE_TOPIC = "/world/default/pose/info"

# Frame global (coincide con el mundo de gz en este escenario) y frame del
# robot cuyo pose se toma del árbol TF como 'initial_pose'.
MAP_FRAME = "map"
ROBOT_FRAME = "camera_link"

# Reglas etiqueta_del_VLM -> modelos de gz. Se busca por subcadena en
# minúsculas; si una regla casa con varios modelos (p.ej. las 4 cajas) se usa
# el CENTROIDE del grupo como ground-truth del objeto.
GT_OBJETOS = [
    {"keywords": ["buzon", "buzón", "postbox", "mailbox", "mail box", "correos", "post box"],
     "modelos": ["postbox"]},
    {"keywords": ["persona", "person", "hombre", "man", "people", "gente", "human"],
     "modelos": ["person_standing"]},
]
