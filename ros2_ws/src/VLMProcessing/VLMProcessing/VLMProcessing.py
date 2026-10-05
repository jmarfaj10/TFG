import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String
from sensor_msgs.msg import Image
from interfaces.msg import Request
from interfaces.msg import Response
import VLMProcessing.constants as constants
import requests
import json
import base64
import cv2
import numpy as np
from cv_bridge import CvBridge
import time
from rclpy.duration import Duration
from tf2_ros import Buffer, TransformListener, TransformException
import tf2_geometry_msgs 
from geometry_msgs.msg import PointStamped
import math

class VLMProcessing(Node):
    def __init__(self):

        super().__init__('VLMProcessing')

        if not self.get_parameter('use_sim_time').get_parameter_value().bool_value:
            self.set_parameters(
                [Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        self.api_url = constants.API_URL
        self.model_name = constants.MODEL_NAME

        #opencv
        self.bridge = CvBridge()

        if self.api_url and self.model_name:
            self.get_logger().info(
                f"Servidor configurado: {self.api_url} ({self.model_name})")
        else:
            self.get_logger().error("Faltan api_url o model_name en el config.yaml")

        self.sub_pet = self.create_subscription(Request, constants.COMM_CHANNEL_VLM, self.pet_VLM, 10)

        self.pub_det = self.create_publisher(Response, constants.GOAL_CHANNEL_VLM, 10)

        self.pub_resp = self.create_publisher(String, constants.RESPONSE_CHANNEL_VLM, 10)

        self.request = None

        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)

    def pet_VLM(self, request):
        self.request = request
        texto_peticion = request.request
        self.get_logger().info(f"Petición recibida del robot: \"{texto_peticion}\"")

        rgb = request.img.img_rgb

        img_b64 = self.codificarBase64(rgb)
        if not img_b64:
            self.get_logger().error("Abortada: no se pudo codificar la imagen.")
            return

        respuesta = self.llamarApi(img_b64, texto_peticion)
        if not respuesta:
            self.get_logger().error("Sin respuesta válida del servidor.")
            return

        datos = self.parsearRespuesta(respuesta)
        if datos is None:
            return
        
        respuesta_texto = datos.get("reply", "")
        deteccion = datos.get("detection", {})

        self.pub_resp.publish(String(data=json.dumps({
    "type": "vlm_response", "data": respuesta_texto})))

        if deteccion:
            img_bbox = self.pintarBBox(rgb, deteccion)

            punto = self.transformarCooredenadas(deteccion)
            self.send_response(punto, respuesta_texto, deteccion["label"], img_bbox)
        else:
            self.get_logger().info("ℹEl modelo no devolvió detecciones.")

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

        if point is None or not math.isfinite(float(point[2])):
            label = deteccion.get("label") or "the object"
            self._notify_user(
                f"I can see {label} in the image, but the depth camera returns "
                "no valid measurements there, so I cannot tell where it is or "
                "move towards it.")
            return
        
        z = float(point[2])
        if depth_msg.encoding in ("16UC1", "mono16"):
            z = z / 1000.0

        xr = ((point[0] - cx) * z) / fx
        yr = ((point[1] - cy) * z) / fy

        self.get_logger().info(f"Punto del objeto en relativo: (x = {xr}, y = {yr}, z = {z})")

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

    def _notify_user(self, text):
        self.get_logger().warn(text)
        self.pub_resp.publish(String(data=json.dumps({
    "type": "vlm_response", "data": text})))

    def _aplicar_standoff(self, punto_obj):
        if punto_obj is None:
            return None
        robot = self._pose_robot_map()
        if robot is None:
            self.get_logger().warn(
                "Sin pose del robot; se usa el punto del objeto como goal "
                "(puede caer sobre el obstáculo).")
            return (punto_obj, 0.0)

        dx = punto_obj[0] - robot[0]
        dy = punto_obj[1] - robot[1]
        dist = math.hypot(dx, dy)
        if dist < 1e-3:
            return ((robot[0], robot[1], robot[2]), 0.0)

        yaw = math.atan2(dy, dx)
        f = (dist - constants.STANDOFF_M) / dist
        goal = (robot[0] + dx * f, robot[1] + dy * f, robot[2])
        self.get_logger().info(
            f"Goal con standoff {constants.STANDOFF_M} m: objeto a {dist:.2f} m "
            f"-> goal=({goal[0]:.2f}, {goal[1]:.2f}, yaw={math.degrees(yaw):.1f}°)")
        return (goal, yaw)
    
    def _pose_robot_map(self):
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

    def send_response(self, target, respuesta_texto, objeto, bbox_image):
        if target is None:
            self.get_logger().warn(
                "No se pudo obtener el punto 3D; no se envía goal.")
            return
        point, yaw = target
        msg = Response()
        msg.response = respuesta_texto
        msg.object = objeto
        msg.x = float(point[0])
        msg.y = float(point[1])
        msg.z = float(point[2])
        msg.yaw = float(yaw)
        if bbox_image is not None:
            msg.bbox_object = bbox_image
        self.pub_det.publish(msg)
        self.get_logger().info(
            f"Detección enviada: objeto={msg.object} "
            f"punto=({msg.x:.2f}, {msg.y:.2f}, {msg.z:.2f}) "
            f"yaw={math.degrees(msg.yaw):.1f}°")

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

        self.get_logger().info(f"POST -> {url}")
        self.get_logger().info(f"   modelo: {self.model_name}")
        self.get_logger().info(f"   tamaño del cuerpo JSON: ~{len(json.dumps(data))/1024:.1f} KB")

        try:
            self.get_logger().info("   Enviando petición (timeout 60s)...")
            t0 = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=60)
            dt = time.time() - t0
            self.get_logger().info(
                f"   Respuesta en {dt:.1f}s | HTTP {response.status_code}")

            if response.status_code != 200:
                self.get_logger().error(f"   El servidor devolvió error:\n{response.text[:1000]}")
                return None

            try:
                parsed = response.json()
            except ValueError:
                self.get_logger().error(
                    f"   La respuesta no es JSON válido:\n{response.text[:1000]}")
                return None

            self.get_logger().info(f"   Respuesta JSON:\n{json.dumps(parsed, indent=2)[:1500]}")
            return parsed

        except requests.exceptions.ConnectTimeout:
            self.get_logger().error("   Timeout al CONECTAR. El servidor no responde "
                                    "(¿IP/puerto correctos? ¿accesible desde el contenedor?).")
        except requests.exceptions.ReadTimeout:
            self.get_logger().error("   Timeout de LECTURA. Conectó pero tardó >60s en responder.")
        except requests.exceptions.ConnectionError as e:
            self.get_logger().error(f"   Error de conexión (servidor caído/inaccesible): {e}")
        except Exception as e:
            self.get_logger().error(f"   Error inesperado en la petición: {e}")
        return None

    def parsearRespuesta(self, respuesta):
        if 'choices' not in respuesta:
            self.get_logger().warn("La respuesta no tiene el campo 'choices' esperado...")
            return None

        try:
            content = respuesta['choices'][0]['message']['content']
            self.get_logger().info(f"Contenido del modelo:\n{content}")

            clean_content = content.replace('```json', '').replace('```', '').strip()
            datos = json.loads(clean_content)

            if datos.get("detection"):
                self.get_logger().info(f"Objeto detectado: {datos.get('detection')}")
            return datos

        except Exception as e:
            self.get_logger().error(f"Error procesando JSON del servidor: {e}")
            return None

    def _dibujar_bbox(self, imagen, deteccion, color):
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

    def pintarBBox(self, rgb_msg, deteccion):
        MAGENTA = (255, 0, 255)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, desired_encoding='bgr8')

            self._dibujar_bbox(cv_image, deteccion, MAGENTA)

            params = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
            success, buffer = cv2.imencode('.jpg', cv_image, params)
            if not success:
                self.get_logger().error("No se pudo codificar la imagen con la bbox a JPEG")
                return ""

            return base64.b64encode(buffer).decode('utf-8')

        except Exception as e:
            self.get_logger().error(f"Error al pintar la bbox: {e}")
            return ""

        
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
