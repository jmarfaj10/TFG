import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
import json
import robotCommunication.constants as constants
from interfaces.action import Move
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
from rclpy.action import ActionClient
from interfaces.msg import Request
from interfaces.msg import Response
from interfaces.msg import ComboImage
from cv_bridge import CvBridge
from tf2_ros import Buffer, TransformListener
from rclpy.time import Time
import message_filters
import time



class RobotCommunication(Node):

    def __init__(self):
        super().__init__('robotCommunication')

        if not self.get_parameter('use_sim_time').get_parameter_value().bool_value:
            self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        self.bridge = CvBridge()

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.map_frame = "map"          
        self.depth_frame = None         

        #MOVE COMMS
        self.client_goal = ActionClient(self, Move, constants.GOAL_CHANEL_ACTION)

        #VLM COMMS
        self.pub_pet = self.create_publisher(Request, constants.COMM_CHANNEL_VLM, 10)
        self.vlm_res = self.create_subscription(Response, constants.GOAL_CHANNEL_VLM, self.recv_vlm, 10)

        #USER COMMS
        self.sub_usercomm = self.create_subscription(String, constants.USER_CHANNEL_COMM, self.userRequest, 10)
        self.pub_usercomm = self.create_publisher(String, constants.RESPONSE_CHANNEL_VLM, 10)

        #OBJETO FINAL
        self.pub_final = self.create_publisher(String, constants.FINAL_CHANNEL, 10)
        self.pub_goal = self.create_publisher(String, constants.GOAL_CHANNEL, 10)

        #CÁMARA
        from rclpy.qos import qos_profile_sensor_data
        rgb_sub        = message_filters.Subscriber(self, Image,      constants.RGB_TOPIC, qos_profile=qos_profile_sensor_data)
        depth_sub      = message_filters.Subscriber(self, Image,      constants.DEPTH_TOPIC, qos_profile=qos_profile_sensor_data)
        rgb_info_sub   = message_filters.Subscriber(self, CameraInfo, constants.RGB_INFO_TOPIC, qos_profile=qos_profile_sensor_data)

        if constants.RGB_INFO_TOPIC == constants.DEPTH_INFO_TOPIC:
            self.sync = message_filters.ApproximateTimeSynchronizer(
                [rgb_sub, depth_sub, rgb_info_sub],
                queue_size=20,
                slop=0.2
            )
            self.sync.registerCallback(lambda r, d, i: self.recvCam(r, d, i, i))
        else:
            depth_info_sub = message_filters.Subscriber(self, CameraInfo, constants.DEPTH_INFO_TOPIC, qos_profile=qos_profile_sensor_data)
            self.sync = message_filters.ApproximateTimeSynchronizer(
                [rgb_sub, depth_sub, rgb_info_sub, depth_info_sub],
                queue_size=20,
                slop=0.2
            )
            self.sync.registerCallback(self.recvCam)

        self.img_pub = self.create_publisher(ComboImage, constants.IMG_CHANNEL, 10)

        self.lastImage = None

        self.init_time = None
        self.final = {"prompt": None, "response": None, "target": None,
                      "initialPose": None, "goalEstimated": None, "finalPose": None,
                      "reachTime": None, "distance": None}

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
    def send_goal(self, x, y, z, yaw, object, bbox_object):

        self.current_goal = {}
        goal = Move.Goal()
        goal.x_goal = float(x)
        goal.y_goal = float(y)
        goal.z_goal = float(z)
        goal.yaw_goal = float(yaw)

        self.current_goal["goal_pose"] = {"x": goal.x_goal, "y": goal.y_goal, "z": goal.z_goal}
        self.current_goal["target"] = object
        self.current_goal["bbox_image"] = bbox_object

        # Goal estimado por el VLM (lo que llega desde VLMProcessing).
        self.final["goalEstimated"] = (goal.x_goal, goal.y_goal, goal.z_goal)
        self.final["initialPose"] = self.get_camera_pose()

        if not self.client_goal.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("El servidor de la action 'move' no está disponible.")
            return
        
        future = self.client_goal.send_goal_async(goal,feedback_callback=self.moveFeedback)
        future.add_done_callback(self.moveResponse)  # ¿aceptado/rechazado?
    
    #MOVE ACTION
    def moveResponse(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Goal rechazado por el servidor.")
            self.pub_goal.publish(String(data=json.dumps(self.current_goal)))
            self.pub_usercomm.publish(String(data=json.dumps({
            "type": "notify", "data": "Robot cannot trace a route for the object."})))
            self.pub_final.publish(String(data=json.dumps({
                "state": "REJECTED",
                "distance": None,
                "final_pose": (None, None, None),
                "time": int(time.time() * 1000) - self.init_time,
            })))
            return
        goal_handle.get_result_async().add_done_callback(self.moveResult)
        self.pub_goal.publish(String(data=json.dumps(self.current_goal)))

    def moveResult(self, future):
        result = future.result()
        result = result.result
        self.final["reachTime"]=int(time.time() * 1000)-self.init_time
        match result.outcome:
            case "REACHED":
                self.final["finalPose"] = (result.x, result.y, result.z)
                self.final["distance"] = result.distancia
                self.get_logger().info(f"Movimiento terminado. distancia={result.distancia:.2f}")
                self.pub_usercomm.publish(String(data=json.dumps({
                "type": "notify", "data": "The robot has reached the goal."})))
                pass
            case "NOT_REACHED":
                self.final["finalPose"] = self.get_camera_pose()
                self.final["distance"] = result.distancia
                self.get_logger().info("Movimiento no terminado.")
                self.pub_usercomm.publish(String(data=json.dumps({
                "type": "notify", "data": "The robot has not reached the goal."})))
                pass
            case "NO_ROUTE":
                self.final["finalPose"] = (None, None, None)
                self.final["distance"] = 0.0
                self.get_logger().info("Meta no calculada.")
                self.pub_usercomm.publish(String(data=json.dumps({
                "type": "notify", "data": "The robot cannot find a path to the goal."})))
                pass
            case _:
                self.get_logger().warn("Estado no reconocido.")
                self.final["finalPose"] = (None, None, None)
                self.final["distance"] = 0.0

        if result.outcome in ["REACHED", "NOT_REACHED", "NO_ROUTE"]:
            final_data = dict(self.final)
            final_data["state"] = result.outcome
            final_data["final_pose"] = self.final["finalPose"]
            final_data["time"] = self.final["reachTime"]

            self.pub_final.publish(String(data=json.dumps(final_data)))
        else:
            return

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
        yaw = msg.yaw
        bbox_image = msg.bbox_object

        self.get_logger().info(f"[RESPUESTA DEL VLM detección: {object}]: {response}\n\n GOAL: (x = {x}, y= {y}, z= {z})")

        self.send_goal(x, y, z, yaw, object, bbox_image)

        self.final["response"] = response
        self.final["target"] = object

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
        self.final["prompt"] = msg.data
        self.pub_pet.publish(request)

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
