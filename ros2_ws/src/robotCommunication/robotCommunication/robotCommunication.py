import rclpy
from rclpy.node import Node
import robotCommunication.constants as constants
from interfaces.action import Move
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from interfaces.msg import Request
from interfaces.msg import Response
from interfaces.msg import ComboImage
from cv_bridge import CvBridge
from tf2_ros import Buffer, TransformListener
from rclpy.time import Time
import message_filters
import time
import math
import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

class Goal:
    def __init__(self):
        self.pose = None
        self.status = None
        

class Final:
    def __int__(self):
        self.distance = None
        self.time = None
        self.final_pose = None

class RobotCommunication(Node):

    def __init__(self):
        super().__init__('robotCommunication')

        self.bridge = CvBridge()

        #TF (para consultar poses en el árbol de transformaciones)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.map_frame = "map"          # frame de referencia global (Nav2)
        self.depth_frame = None         # se rellena al recibir el primer CameraInfo

        #MOVE COMMS
        self.client_goal = ActionClient(self, Move, constants.GOAL_CHANEL_ACTION)

        #VLM COMMS
        self.pub_pet = self.create_publisher(Request, constants.COMM_CHANNEL_VLM, 10)
        self.vlm_res = self.create_subscription(Response, constants.GOAL_CHANNEL_VLM, self.recv_vlm, 10)

        #USER COMMS
        # Entrada: peticiones del usuario. Salida: respuestas/estado hacia el
        # usuario en un canal DISTINTO (si publicáramos en USER_CHANNEL_COMM
        # nos llegarían de vuelta a userRequest -> bucle infinito de goals).
        self.sub_usercomm = self.create_subscription(String, constants.USER_CHANNEL_COMM, self.userRequest, 10)
        self.pub_usercomm = self.create_publisher(String, constants.RESPONSE_CHANNEL_VLM, 10)

        #LOGGER
        self.pub_final = self.create_publisher(Final, constants.FINAL_CHANNEL, 10)
        self.pub_goal = self.create_publisher(Goal, constants.GOAL_CHANNEL, 10)

        #CÁMARA
        rgb_sub        = message_filters.Subscriber(self, Image,      constants.RGB_TOPIC)
        depth_sub      = message_filters.Subscriber(self, Image,      constants.DEPTH_TOPIC)
        rgb_info_sub   = message_filters.Subscriber(self, CameraInfo, constants.RGB_INFO_TOPIC)
        depth_info_sub = message_filters.Subscriber(self, CameraInfo, constants.DEPTH_INFO_TOPIC)

        self.sync = message_filters.ApproximateTimeSynchronizer(
            [rgb_sub, depth_sub, rgb_info_sub, depth_info_sub],
            queue_size=10,
            slop=0.05
        )

        self.sync.registerCallback(self.recvCam)

        self.img_pub = self.create_publisher(ComboImage, constants.IMG_CHANNEL, 10)

        self.lastImage = None

        #Parametros para el logger
        self.declare_parameter('debug', False)
        self.debug = self.get_parameter('debug').get_parameter_value().bool_value

        self.init_time = None
        self.logger = {"prompt": None, "response": None, "tarjet": None, "initialPose": None, "finalPose": None, "gt": None, "reachTime": None, "distance":None}

        self.gt_modelos = None

        self.current_goal = None

        self.last_final = None

    #CAM TOPIC
    def recvCam(self, imgRgb, imgDepth, rgbCameraInfo, depthCameraInfo):
        height = None
        width  = None

        if depthCameraInfo.height == rgbCameraInfo.height:
            height = rgbCameraInfo.height

        if depthCameraInfo.width == rgbCameraInfo.width:
            width = rgbCameraInfo.width

        height = height if height is not None else 0
        width = width if width is not None else 0

        depth_k = depthCameraInfo.k
        self.depth_frame = depthCameraInfo.header.frame_id

        self.depth_width = imgDepth.width
        self.depth_height = imgDepth.height

        msg = ComboImage()
        msg.fx    = float(depth_k[0])
        msg.fy    = float(depth_k[4])
        msg.cx         = float(depth_k[2])
        msg.cy         = float(depth_k[5])
        msg.img_rgb   = imgRgb
        msg.img_depth = imgDepth

        if msg.fx == 0 or msg.fy == 0:
            return

        self.lastImage = msg
        self.img_pub.publish(msg)

    #POSE DE LA CÁMARA (respecto al frame global 'map')
    def get_camera_pose(self):
        if self.depth_frame is None:
            self.get_logger().warn("Aún no se conoce el frame de la cámara (no ha llegado CameraInfo).")
            return None
        try:
            t = self.tf_buffer.lookup_transform(self.map_frame, self.depth_frame, Time())
            p = t.transform.translation
            return (p.x, p.y, p.z)
        except Exception as e:
            self.get_logger().warn(f"No hay TF {self.map_frame}->{self.depth_frame}: {e}")
            return None

    #MOVE TOPIC
    def send_goal(self, x, y, z):

        self.current_goal = Goal()
        goal = Move.Goal()
        goal.x_goal = float(x)
        goal.y_goal = float(y)
        goal.z_goal = float(z)

        self.current_goal.goal_pose = {"x": goal.x_goal, "y": goal.y_goal, "z": goal.z_goal}

        # Goal estimado por el VLM (lo que llega desde VLMProcessing).
        self.logger["goalEstimated"] = (goal.x_goal, goal.y_goal, goal.z_goal)
        self.logger["initialPose"] = self.get_camera_pose()

        if not self.client_goal.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("El servidor de la action 'move' no está disponible.")
            return
        
        future = self.client_goal.send_goal_async(goal,feedback_callback=self.moveFeedback)   # progreso en vivo
        future.add_done_callback(self.moveResponse)  # ¿aceptado/rechazado?
    
    #MOVE ACTION
    def moveResponse(self, future):
        
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Goal rechazado por el servidor.")
            self.current_goal.status="REJECTED"
            self.pub_goal(self.current_goal)
            return
        self.current_goal.status = "ACCEPTED"
        goal_handle.get_result_async().add_done_callback(self.moveResult)
        self.pub_goal(self.current_goal)

    def moveResult(self, future):
        outcome = future.result()
        if outcome.status != GoalStatus.STATUS_SUCCEEDED:
            return

        result = outcome.result
        self.logger["reachTime"]=int(time.time() * 1000)-self.init_time
        self.logger["finalPose"] = (result.x, result.y, result.z)
        self.logger["distance"] = result.distancia

        self.get_logger().info(f"Movimiento terminado. distancia={result.distancia:.2f}")
        self.pintarLogger()
        self.pub_usercomm.publish(String(data="The robot has reached the goal"))

        final = Final()
        final.distance = result.distancia
        final.final_pose = (result.x, result.y, result.z)
        final.time = int(time.time() * 1000)-self.init_time

        self.pub_logger.publish(final)

    def moveFeedback(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f"En camino: x={fb.x_current:.2f} y={fb.y_current:.2f}",
            throttle_duration_sec=1.0)

    #VLM TOPIC
    def recv_vlm(self, msg):
        if not msg:
            self.get_logger().error("No hay respuesta del VLM")
            return

        response = msg.response
        object = msg.object
        x = msg.x
        y = msg.y
        z = msg.z

        self.get_logger().info(f"[RESPUESTA DEL VLM detección: {object}]: {response}\n\n GOAL: (x = {x}, y= {y}, z= {z})")

        # Posición real del objeto en la simulación (ground-truth de Gazebo),
        # para poder compararla con el goal estimado por el VLM en el logger.
        self.logger["gt"] = self._gt_objeto(object)

        self.send_goal(x, y, z)
        # La respuesta en texto ya la publica VLMProcessing en RESPONSE_CHANNEL_VLM,
        # así que no la reenviamos aquí para no duplicarla al usuario.

        self.logger["response"] = response
        self.logger["tarjet"] = object

    #USER TOPIC
    def userRequest(self, msg):
        
        self.init_time = int(time.time() * 1000)
        request= Request()
        if self.lastImage == None:
            self.get_logger().error("No se puede enviar la petición porque no hay imagen")
            return

        self.initialPose = self.get_camera_pose()
        if not msg.data.strip():
            self.get_logger().error("No se ha introducido ningún mensaje")
            return
        
        combo = ComboImage()

        combo.cx = self.lastImage.cx
        combo.cy = self.lastImage.cy
        combo.img_depth = self.lastImage.img_depth
        combo.img_rgb = self.lastImage.img_rgb
        combo.fx = self.lastImage.fx
        combo.fy = self.lastImage.fy
        request.img = combo
        request.request = msg.data
        self.logger["prompt"] = msg.data
        self.pub_pet.publish(request)

    #--LOGS METHODS--

    #GROUND-TRUTH DE LA SIMULACIÓN
    def _cargar_gt_modelos(self):
        """Consulta a Gazebo (gz-transport) las poses de todos los modelos del
        mundo y las cachea por nombre. Devuelve dict {nombre: (x, y, z)} o None
        si falla."""
        gz = shutil.which("gz")
        if not gz:
            self.get_logger().warn(
                "No se encontró el CLI 'gz' en el PATH; no hay posición real de "
                "objetos (columna 'Real Goal' quedará vacía).")
            return None
        try:
            salida = subprocess.run(
                [gz, "topic", "-e", "-t", constants.GZ_POSE_TOPIC, "-n", "1"],
                capture_output=True, text=True, timeout=10).stdout
        except (subprocess.TimeoutExpired, OSError) as e:
            self.get_logger().warn(f"No se pudo leer la posición real de gz: {e}")
            return None

        modelos = {}
        for bloque in re.split(r'\npose\s*{', salida):
            nm = re.search(r'name:\s*"([^"]+)"', bloque)
            pos = re.search(r'position\s*{([^}]*)}', bloque)
            if not nm or not pos:
                continue
            vals = {}
            for k in ("x", "y", "z"):
                m = re.search(rf'\b{k}:\s*([-\d.eE]+)', pos.group(1))
                vals[k] = float(m.group(1)) if m else 0.0
            modelos[nm.group(1)] = (vals["x"], vals["y"], vals["z"])

        self.get_logger().info(f"Posición real cargada: {len(modelos)} modelos de gz.")
        return modelos

    def _gt_objeto(self, objeto):
        """Posición real (x, y, z) del objeto detectado, mapeando la etiqueta
        del VLM a los modelos de gz (centroide si son varios). None si no hay
        match."""
        if self.gt_modelos is None:
            self.gt_modelos = self._cargar_gt_modelos()
        if not self.gt_modelos:
            return None

        etiqueta = (objeto or "").lower()
        patrones = None
        for regla in constants.GT_OBJETOS:
            if any(kw in etiqueta for kw in regla["keywords"]):
                patrones = regla["modelos"]
                break
        if patrones is None:
            self.get_logger().warn(
                f"Sin regla de posición real para el objeto '{objeto}'.")
            return None

        casados = [p for nombre, p in self.gt_modelos.items()
                    if any(pat in nombre.lower() for pat in patrones)]
        if not casados:
            self.get_logger().warn(
                f"No hay modelos de gz que casen con {patrones} para '{objeto}'.")
            return None

        n = len(casados)
        centroide = (sum(p[0] for p in casados) / n,
                    sum(p[1] for p in casados) / n,
                    sum(p[2] for p in casados) / n)
        self.get_logger().info(
            f"Posición real de '{objeto}': {n} modelo(s) -> centroide {centroide}")
        return centroide

    @staticmethod
    def _dist(a, b):
        """Distancia euclídea 3D entre dos puntos (x, y, z). None si falta alguno."""
        if a is None or b is None:
            return None
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

    def pintarLogger(self):
        cabecera = ["Prompt", "Response", "Tarjet", "initial pose","Goal estimated", "Ground Truth", "Travel Time", "Distance traveled"]

        ruta = os.path.expanduser("~/src-local-ros-logger-exp2.csv")

        existe = Path(ruta).exists()

        claves = list(self.logger.keys())

        if not existe:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(cabecera)
        with open(ruta, "a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow([self.logger[k] for k in claves])   # una fila con los valores

def main(args=None):
    rclpy.init(args=args)
    node = RobotCommunication()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
