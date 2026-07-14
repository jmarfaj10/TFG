import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String
from sensor_msgs.msg import Image
from interfaces.msg import Request
from interfaces.msg import Response
import VLMProcessing.constants as constants
import message_filters
import requests
import json
import base64
import os
import cv2
import numpy as np
from cv_bridge import CvBridge
import time
from rclpy.duration import Duration
from tf2_ros import Buffer, TransformListener, TransformException
import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped
import math
import csv
import re
import shutil
import subprocess
from pathlib import Path

class VLMProcessing(Node):
    def __init__(self):

        super().__init__('VLMProcessing')

        # Entorno de simulación (Gazebo): TF y sensores se publican en tiempo
        # de simulación. Sin esto el nodo usa wall-time y las consultas a TF
        # fallan con "extrapolation into the past" (dominios de reloj distintos).
        # Se puede sobreescribir al lanzar con -p use_sim_time:=false.
        if not self.get_parameter('use_sim_time').get_parameter_value().bool_value:
            self.set_parameters(
                [Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        #Cargar constantes (servidor VLM desde config.yaml)
        self.api_url = constants.API_URL
        self.model_name = constants.MODEL_NAME

        #opencv
        self.bridge = CvBridge()

        if self.api_url and self.model_name:
            self.get_logger().info(
                f"✅ Servidor configurado: {self.api_url} ({self.model_name})")
        else:
            self.get_logger().error("❌ Faltan api_url o model_name en el config.yaml")

        # robotCommunication -> VLMProcessing
        self.sub_pet = self.create_subscription(Request, constants.COMM_CHANNEL_VLM, self.pet_VLM, 10)

        # VLMProcessing -> robotCommunication
        self.pub_det = self.create_publisher(Response, constants.GOAL_CHANNEL_VLM, 10)

        # VLMProcessing -> userCommunication
        self.pub_resp = self.create_publisher(String, constants.RESPONSE_CHANNEL_VLM, 10)
        
        self.request = None

        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)

        # Ground-truth de los objetos (estáticos) del mundo, leído una vez de
        # Gazebo y cacheado: {nombre_modelo: (x, y, z)}.

        #loggers
        self.gt_modelos = None

        self.declare_parameter('debug', False)
        self.debug = self.get_parameter('debug').get_parameter_value().bool_value

        self.logger = {"prompt": None, "initial_pose_r": None, "initial_pose": None, "object_pose_r": None, "object_pose": None, "distance_vlm": None, "distance": None, "error": None}

        self.logger["initial_pose_r"] = (0,0,0)

    def pet_VLM(self, request):
        self.request = request
        texto_peticion = request.request
        self.logger["prompt"] = texto_peticion
        self.get_logger().info(f"🚀 Petición recibida del robot: \"{texto_peticion}\"")

        rgb = request.img.img_rgb

        img_b64 = self.codificarBase64(rgb)
        if not img_b64:
            self.get_logger().error("Abortada: no se pudo codificar la imagen.")
            return

        respuesta = self.llamarApi(img_b64, texto_peticion)
        if not respuesta:
            self.get_logger().error("❌ Sin respuesta válida del servidor.")
            return

        datos = self.parsearRespuesta(respuesta)
        if datos is None:
            return
        
        respuesta_texto = datos.get("reply", "")
        deteccion = datos.get("detection", {})

        # VLMProcessing -> userCommunication (respuesta en texto al usuario)
        resp_msg = String()
        resp_msg.data = respuesta_texto
        self.pub_resp.publish(resp_msg)

        if deteccion:
            self.pintarBBox(rgb, deteccion)

            punto = self.transformarCooredenadas(deteccion)

            # Ground-truth para el logger: pose del robot (TF) y pose real del
            # objeto detectado (Gazebo). Van al logger antes de pintarLogger.
            self.logger["initial_pose"] = self._pose_robot_map()
            self.logger["object_pose"] = self._gt_objeto(deteccion.get("label"))

            self.pintarLogger()
            self.send_response(punto, respuesta_texto, deteccion["label"])
        else:
            self.get_logger().info("ℹ️  El modelo no devolvió detecciones.")

    def local_to_map(self, local_pose, source_frame):
            if not source_frame:
                self.get_logger().warn(
                    "El mensaje de profundidad no trae frame_id; no se puede "
                    "transformar a 'map'.")
                return None
            self.get_logger().info(f"[TRANSFORMANDO]: {source_frame}")
            p = PointStamped()
            p.header.frame_id = source_frame
            p.header.stamp = rclpy.time.Time().to_msg()
            x_opt, y_opt, z_opt = local_pose
            p.point.x = x_opt 
            p.point.y = y_opt    
            p.point.z = z_opt     

            try:
                r = self.buffer.transform(p, "map", timeout=Duration(seconds=1.0))
                self.get_logger().info(f"Puntos en el mapa: (x = {r.point.x}, y = {r.point.y}, z = {r.point.z})")
                return (r.point.x, r.point.y, r.point.z)
            except TransformException as e:
                self.get_logger().warn(f"No se pudo transformar: {e}")
                return None

    def transformarCooredenadas(self, deteccion):
        x1, y1, x2, y2 = deteccion["bbox"]
        cx = self.request.img.cx
        cy = self.request.img.cy
        fx = self.request.img.fx
        fy = self.request.img.fy
        depth_msg = self.request.img.img_depth
        depth_img = self.bridge.imgmsg_to_cv2(depth_msg)

        # El VLM devuelve el bbox NORMALIZADO 0..VLM_COORD_SCALE (no en
        # píxeles). Hay que des-normalizarlo a píxeles de la imagen de
        # profundidad, que es donde muestreamos y donde valen los
        # intrínsecos cx/cy/fx/fy.
        scale = constants.VLM_COORD_SCALE
        depth_h, depth_w = depth_img.shape[:2]
        bbox = [
            int(x1 / scale * depth_w),
            int(y1 / scale * depth_h),
            int(x2 / scale * depth_w),
            int(y2 / scale * depth_h),
        ]
        self.get_logger().info(
            f"Bbox des-normalizado (0-{scale}) -> depth({depth_w}x{depth_h}): "
            f"{deteccion['bbox']} -> {bbox}")

        point = self.estimarObjeto(depth_img, bbox)

        if point is None:
            self.get_logger().error("No hay suficientes puntos de profundidad validos para estimar el objeto")
            return

        if point[2] == float('inf'):
            self.get_logger().error("Profundidad en infinito no valida")
            return

        # Normalizar a METROS según el encoding de la cámara de profundidad
        # (16UC1/mono16 = milímetros; 32FC1 = metros).
        z = float(point[2])
        if depth_msg.encoding in ("16UC1", "mono16"):
            z = z / 1000.0

        xr = ((point[0] - cx) * z) / fx
        yr = ((point[1] - cy) * z) / fy

        self.get_logger().info(f"Punto del objeto en relativo: (x = {xr}, y = {yr}, z = {z})")

        self.logger["object_pose_r"] = (xr, yr, z)

        # Se usa el frame ÓPTICO de profundidad (no el frame_id del mensaje,
        # que es no-óptico) para que ejes y convención coincidan con el punto.
        punto_obj_glob = self.local_to_map((xr, yr, z), constants.DEPTH_OPTICAL_FRAME)
        return self._aplicar_standoff(punto_obj_glob)
    
    def estimarObjeto(self, depth, bbox):
        x1, y1, x2, y2 = bbox
        w = x2 - x1
        h = y2 - y1
        cx = x1 + w // 2
        cy = y1 + h // 2

        tam_w = 28
        h_img, w_img = depth.shape[:2]
        x0 = max(0, cx - tam_w // 2)
        y0 = max(0, cy - tam_w // 2)
        x1p = min(w_img, cx + tam_w // 2)
        y1p = min(h_img, cy + tam_w // 2)

        parche = depth[y0:y1p, x0:x1p].astype(np.float32)

        valida = (parche > 0.1) & np.isfinite(parche)
        vs, us = np.nonzero(valida)
        d = parche[valida]

        if d.size < 20:
            return None

        hist, bordes = np.histogram(d, bins=50)
        umbral = d.size * 0.05
        idx = np.argmax(hist > umbral)
        d_min, d_max = bordes[idx], bordes[idx + 1]

        sel = (d >= d_min) & (d <= d_max)
        us_c, vs_c, d_c = us[sel], vs[sel], d[sel]

        cu, cv = cx - x0, cy - y0
        dist2 = (us_c - cu) ** 2 + (vs_c - cv) ** 2
        i = np.argmin(dist2)

        u = us_c[i] + x0
        v = vs_c[i] + y0
        z = d_c[i]

        return (u, v, z)

    def _aplicar_standoff(self, punto_obj):
        if punto_obj is None:
            return None
        robot = self._pose_robot_map()
        if robot is None:
            self.get_logger().warn(
                "Sin pose del robot; se usa el punto del objeto como goal "
                "(puede caer sobre el obstáculo).")
            return punto_obj

        dx = punto_obj[0] - robot[0]
        dy = punto_obj[1] - robot[1]
        dist = math.hypot(dx, dy)
        if dist <= constants.STANDOFF_M:
            # El objeto está más cerca que el standoff: no avanzar más.
            self.get_logger().info(
                f"Objeto a {dist:.2f} m (< standoff); goal en la pose actual.")
            return (robot[0], robot[1], robot[2])

        f = (dist - constants.STANDOFF_M) / dist
        goal = (robot[0] + dx * f, robot[1] + dy * f, robot[2])
        self.get_logger().info(
            f"Goal con standoff {constants.STANDOFF_M} m: objeto a {dist:.2f} m "
            f"-> goal=({goal[0]:.2f}, {goal[1]:.2f})")
        return goal
    
    def _pose_robot_map(self):
        """Pose del robot en el frame global, tomado del árbol TF
        (MAP_FRAME -> ROBOT_FRAME). Devuelve (x, y, z) o None."""
        try:
            t = self.buffer.lookup_transform(
                constants.MAP_FRAME, constants.ROBOT_FRAME,
                rclpy.time.Time(), timeout=Duration(seconds=1.0))
            tr = t.transform.translation
            return (tr.x, tr.y, tr.z)
        except TransformException as e:
            self.get_logger().warn(
                f"No se pudo obtener el pose del robot desde TF: {e}")
            return None

    def send_response(self, punto, respuesta_texto, objeto):
        """Publica la detección (texto de respuesta + bbox normalizado 0-1000)
        en GOAL_CHANNEL_VLM. robotCommunication se encarga del paso a 3D
        (deproyección con K + TF a 'map')."""
        if punto is None:
            self.get_logger().warn(
                "No se pudo obtener el punto 3D; no se envía goal.")
            return
        msg = Response()
        msg.response = respuesta_texto
        msg.object = objeto
        msg.x = float(punto[0])
        msg.y = float(punto[1])
        msg.z = float(punto[2])
        self.pub_det.publish(msg)
        self.get_logger().info(
            f"📦 Detección enviada: objeto={msg.object} "
            f"punto=({msg.x:.2f}, {msg.y:.2f}, {msg.z:.2f})")

    def codificarBase64(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            small_img = cv2.resize(cv_image, (0, 0), fx=0.5, fy=0.5)

            params = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
            success, buffer = cv2.imencode('.jpg', small_img, params)

            if success:
                return base64.b64encode(buffer).decode('utf-8')

        except Exception as e:
            self.get_logger().error(f"Error al comprimir/codificar: {str(e)}")
            return None

    def llamarApi(self, img_codf, pregunta):
        prompt_completo = f"""
                        Act as the assistant of a robot with computer vision.
                        User message: "{pregunta}"
                        ALWAYS return a JSON with two fields:
                            - "reply": plain text answering the user naturally.
                            - "detection": the object requested to be located.
                        Instructions:
                            - LANGUAGE (most important rule): detect the language of the User message above and write the "reply" field in THAT SAME language. If the user writes in Spanish, "reply" must be in Spanish; if in English, in English, etc. Never switch languages.
                            - If the user asks to locate an object and it appears in the image, include it in "detection" with its bbox and explain in "reply" what you found.
                            - If the message does NOT ask to locate an object (e.g. a greeting) or the object does not appear, "detection" must be {{}} and "reply" contains your reply to the user.
                            - Detect ONLY the object the user asks for; do not make up objects.
                            - Reply DIRECTLY with the JSON, with no text outside the JSON.
                            - The bbox is [x1, y1, x2, y2] where (x1,y1) is the top-left corner and (x2,y2) the bottom-right corner, with NORMALIZED INTEGER values from 0 to 1000 relative to the width (x coordinate) and the height (y coordinate) of the image.
                            - Format: {{"reply": "...", "detection": {{"label": "name", "bbox": [x1, y1, x2, y2]}}}}
                        """

        url = self.api_url.rstrip('/') + "/chat/completions"

        headers = {"Content-Type": "application/json"}

        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a robot assistant. You MUST always write the "
                        "\"reply\" field in the exact same language as the "
                        "user's message. Match the user's language; never "
                        "translate or switch to another language."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_completo},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_codf}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 150,
            "top_p": 0.8,
            "extra_body": {
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            }
        }

        self.get_logger().info(f"🌐 POST -> {url}")
        self.get_logger().info(f"   modelo: {self.model_name}")
        self.get_logger().info(f"   tamaño del cuerpo JSON: ~{len(json.dumps(data))/1024:.1f} KB")

        try:
            self.get_logger().info("   ⏱️  Enviando petición (timeout 60s)...")
            t0 = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=60)
            dt = time.time() - t0
            self.get_logger().info(
                f"   📥 Respuesta en {dt:.1f}s | HTTP {response.status_code}")

            if response.status_code != 200:
                self.get_logger().error(f"   ❌ El servidor devolvió error:\n{response.text[:1000]}")
                return None

            try:
                parsed = response.json()
            except ValueError:
                self.get_logger().error(
                    f"   ❌ La respuesta no es JSON válido:\n{response.text[:1000]}")
                return None

            self.get_logger().info(f"   📄 Respuesta JSON:\n{json.dumps(parsed, indent=2)[:1500]}")
            return parsed

        except requests.exceptions.ConnectTimeout:
            self.get_logger().error("   ❌ Timeout al CONECTAR. El servidor no responde "
                                    "(¿IP/puerto correctos? ¿accesible desde el contenedor?).")
        except requests.exceptions.ReadTimeout:
            self.get_logger().error("   ❌ Timeout de LECTURA. Conectó pero tardó >60s en responder.")
        except requests.exceptions.ConnectionError as e:
            self.get_logger().error(f"   ❌ Error de conexión (servidor caído/inaccesible): {e}")
        except Exception as e:
            self.get_logger().error(f"   ❌ Error inesperado en la petición: {e}")
        return None

    def parsearRespuesta(self, respuesta):
        if 'choices' not in respuesta:
            self.get_logger().warn("La respuesta no tiene el campo 'choices' esperado...")
            return None

        try:
            content = respuesta['choices'][0]['message']['content']
            self.get_logger().info(f"💬 Contenido del modelo:\n{content}")

            clean_content = content.replace('```json', '').replace('```', '').strip()
            datos = json.loads(clean_content)

            if datos.get("detection"):
                self.get_logger().info(f"✅ Objeto detectado: {datos.get('detection')}")
            return datos

        except Exception as e:
            self.get_logger().error(f"Error procesando JSON del servidor: {e}")
            return None

    #LOGGERS

    def _cargar_gt_modelos(self):
        """Consulta a Gazebo (gz-transport) los poses de todos los modelos del
        mundo y los cachea por nombre. Los objetos son estáticos, así que basta
        una lectura. Devuelve dict {nombre: (x, y, z)} o None si falla."""
        gz = shutil.which("gz")
        if not gz:
            self.get_logger().warn(
                "No se encontró el CLI 'gz' en el PATH; no hay ground-truth de "
                "objetos (columnas globales quedarán vacías).")
            return None
        try:
            salida = subprocess.run(
                [gz, "topic", "-e", "-t", constants.GZ_POSE_TOPIC, "-n", "1"],
                capture_output=True, text=True, timeout=10).stdout
        except (subprocess.TimeoutExpired, OSError) as e:
            self.get_logger().warn(f"No se pudo leer el ground-truth de gz: {e}")
            return None

        modelos = {}
        # El mensaje Pose_V se imprime como bloques 'pose { name: "..."
        # position { x: .. y: .. z: .. } ... }'.
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

        self.get_logger().info(f"Ground-truth cargado: {len(modelos)} modelos de gz.")
        return modelos

    def _gt_objeto(self, objeto):
        """Ground-truth (x, y, z) del objeto detectado, mapeando la etiqueta del
        VLM a los modelos de gz (centroide si son varios). None si no hay match."""
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
                f"Sin regla de ground-truth para el objeto '{objeto}'.")
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
            f"GT objeto '{objeto}': {n} modelo(s) -> centroide {centroide}")
        return centroide

    def _dibujar_bbox(self, imagen, deteccion, color):
        """Dibuja sobre 'imagen' (BGR) el recuadro de la bbox y la etiqueta del
        objeto en el 'color' dado (BGR). La bbox llega normalizada 0-scale, así
        que se escala a las dimensiones de la imagen recibida."""
        H, W = imagen.shape[:2]
        scale = constants.VLM_COORD_SCALE

        x1, y1, x2, y2 = deteccion["bbox"]
        px1 = int(x1 / scale * W)
        py1 = int(y1 / scale * H)
        px2 = int(x2 / scale * W)
        py2 = int(y2 / scale * H)

        # Mantener los puntos dentro de la imagen.
        px1 = max(0, min(W - 1, px1))
        py1 = max(0, min(H - 1, py1))
        px2 = max(0, min(W - 1, px2))
        py2 = max(0, min(H - 1, py2))

        cv2.rectangle(imagen, (px1, py1), (px2, py2), color, 2)

        etiqueta = str(deteccion.get("label", ""))
        if etiqueta:
            cv2.putText(imagen, etiqueta, (px1, max(0, py1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    def _depth_a_bgr(self, depth_msg):
        """Convierte la imagen de profundidad a una imagen BGR visualizable:
        normaliza a 0-255 (ignorando NaN/inf) y aplica un colormap."""
        depth = self.bridge.imgmsg_to_cv2(depth_msg)
        depth = np.nan_to_num(depth.astype(np.float32),
        nan=0.0, posinf=0.0, neginf=0.0)
        depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        depth_u8 = depth_norm.astype(np.uint8)
        return cv2.applyColorMap(depth_u8, cv2.COLORMAP_JET)

    def _guardar_imagen(self, carpeta, nombre, imagen):
        """Guarda 'imagen' en carpeta/nombre y registra el resultado."""
        ruta = os.path.join(carpeta, nombre)
        if cv2.imwrite(ruta, imagen):
            self.get_logger().info(f"🖼️  Imagen guardada en: {ruta}")
        else:
            self.get_logger().error(f"No se pudo guardar la imagen en: {ruta}")
        return ruta

    def pintarBBox(self, rgb_msg, deteccion):
        """Guarda cuatro imágenes en ~/bbox-snapshoots con el mismo timestamp:
        la RGB y la de profundidad, cada una con la bbox (magenta) y sin ella
        (sufijo '_raw'). Devuelve la ruta de la RGB con bbox."""
        # Magenta en BGR (el formato de OpenCV).
        MAGENTA = (255, 0, 255)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, desired_encoding='bgr8')

            # cv2.imwrite NO crea directorios; hay que asegurarse de que exista
            # (y usar una ruta bajo $HOME, no '/bbox-snapshoots' en la raíz, que
            # requeriría permisos de root).
            carpeta = os.path.expanduser('~/bbox-snapshoots')
            os.makedirs(carpeta, exist_ok=True)

            # Base de nombre común a la pareja RGB/profundidad.
            base = f"bbox_{int(time.time())}"

            # RGB: primero sin bbox ('_raw'), luego con la bbox dibujada.
            self._guardar_imagen(carpeta, f"{base}_raw.jpg", cv_image)
            self._dibujar_bbox(cv_image, deteccion, MAGENTA)
            ruta = self._guardar_imagen(carpeta, f"{base}.jpg", cv_image)

            # Profundidad: misma lógica, con el prefijo 'depth-'.
            try:
                depth_bgr = self._depth_a_bgr(self.request.img.img_depth)
                self._guardar_imagen(carpeta, f"depth-{base}_raw.jpg", depth_bgr)
                self._dibujar_bbox(depth_bgr, deteccion, MAGENTA)
                self._guardar_imagen(carpeta, f"depth-{base}.jpg", depth_bgr)
            except Exception as e:
                self.get_logger().error(
                    f"Error al guardar la imagen de profundidad: {e}")

            return ruta

        except Exception as e:
            self.get_logger().error(f"Error al pintar/guardar la bbox: {e}")
            return None
        
    @staticmethod
    def xyz(pose):
        """Normaliza un pose a (x, y, z). Acepta tuplas/listas o
        geometry_msgs/Transform (que es como llegan los poses de
        ground-truth). Devuelve None si el pose aún no está disponible."""
        if pose is None:
            return None
        if isinstance(pose, (tuple, list)):
            return tuple(pose)
        t = pose.translation      # geometry_msgs/Transform
        return (t.x, t.y, t.z)

    @staticmethod
    def _dist(a, b):
        if a is None or b is None:
            return None
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

    def pintarLogger(self):
        cabecera = ["prompt","initial pose(relative)","initial pose(global)","object pose(relative)","objet pose(global)","distance(relative)","distance(global)","error"]

        # Los poses de ground-truth ('initial_pose'/'object_pose') llegan por
        # /world/default/pose/info y pueden ser None si ese frame aún no se ha
        # publicado (p.ej. el objeto detectado no es 'bus_stop'). No abortamos:
        # registramos lo que haya y dejamos None en el resto.
        obj_r = self.xyz(self.logger["object_pose_r"])
        ini_r = self.xyz(self.logger["initial_pose_r"])
        obj_g = self.xyz(self.logger["object_pose"])
        ini_g = self.xyz(self.logger["initial_pose"])

        self.logger["distance_vlm"] = self._dist(obj_r, ini_r)
        self.logger["distance"] = self._dist(obj_g, ini_g)

        if self.logger["distance"] is not None and self.logger["distance_vlm"] is not None:
            self.logger["error"] = self.logger["distance"] - self.logger["distance_vlm"]
        else:
            self.logger["error"] = None

        ruta = os.path.expanduser("~/src-local-ros-logger-exp1.csv")

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
    node = VLMProcessing()
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
