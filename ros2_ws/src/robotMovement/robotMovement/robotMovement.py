import math
import threading

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor, ExternalShutdownException
from action_msgs.msg import GoalStatus
from nav2_msgs.action import NavigateToPose
from interfaces.action import Move
import robotMovement.constants as constants
from rclpy.action import GoalResponse


class RobotMovement(Node):
    def __init__(self):
        super().__init__('robotMovement')

        cb_group = ReentrantCallbackGroup()

        self.action_server = ActionServer(
            self,
            Move,
            constants.GOAL_CHANEL_ACTION,
            self.mover,
            goal_callback=self.validar_goal,
            callback_group=cb_group)

        self.nav2_client= ActionClient(
            self, NavigateToPose, 'navigate_to_pose',
            callback_group=cb_group)

    def validar_goal(self, request):
        if not all(math.isfinite(v) for v in (request.x_goal, request.y_goal, request.yaw_goal)):
            return GoalResponse.REJECT
        if not self.nav2_client.server_is_ready():
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT
    def mover(self, goal_handle):
        self.get_logger().info('Ejecutando goal...')
        req = goal_handle.request

        nav_goal = NavigateToPose.Goal()
        nav_goal.pose.header.frame_id = "map"
        nav_goal.pose.header.stamp = self.get_clock().now().to_msg()
        nav_goal.pose.pose.position.x = float(req.x_goal)
        nav_goal.pose.pose.position.y = float(req.y_goal)
        nav_goal.pose.pose.position.z = float(req.z_goal)
        yaw = float(req.yaw_goal)
        nav_goal.pose.pose.orientation.z = math.sin(yaw / 2.0)
        nav_goal.pose.pose.orientation.w = math.cos(yaw / 2.0)

        # Estado para acumular la distancia recorrida (Nav2 solo informa de la
        # distancia restante) y quedarnos con la última pose conocida.
        track = {"dist": 0.0, "last": None,
                "x": float(req.x_goal), "y": float(req.y_goal), "z": float(req.z_goal)}

        def nav_feedback_cb(feedback_msg):
            pos = feedback_msg.feedback.current_pose.pose.position
            fb = Move.Feedback()
            fb.x_current = float(pos.x)
            fb.y_current = float(pos.y)
            goal_handle.publish_feedback(fb)

            # Distancia recorrida: sumamos el desplazamiento entre poses
            # consecutivas y guardamos la posición actual como final.
            if track["last"] is not None:
                track["dist"] += math.sqrt(
                    (pos.x - track["last"][0]) ** 2 +
                    (pos.y - track["last"][1]) ** 2 +
                    (pos.z - track["last"][2]) ** 2)
            track["last"] = (pos.x, pos.y, pos.z)
            track["x"] = float(pos.x)
            track["y"] = float(pos.y)
            track["z"] = float(pos.z)

            d = feedback_msg.feedback.distance_remaining
            # throttle: 1 log/seg para no inundar la consola.
            self.get_logger().info(
                f'Nav2 dice: faltan {d:.2f} m',
                throttle_duration_sec=1.0)

        self.nav2_client.wait_for_server()
        self.get_logger().info(
            f'Pasando goal a Nav2: ({req.x_goal}, {req.y_goal}) '
            f'yaw={math.degrees(yaw):.1f}°')

        send_future = self.nav2_client.send_goal_async(
            nav_goal,
            feedback_callback=nav_feedback_cb)
        # El executor multihilo procesa el future en otro hilo; aquí solo
        # esperamos a que termine (no hacer spin anidado sobre el nodo).
        send_done = threading.Event()
        send_future.add_done_callback(lambda _f: send_done.set())
        send_done.wait()
        nav_handle = send_future.result()

        if not nav_handle.accepted:
            self.get_logger().info('Nav2 rechazó el goal')
            goal_handle.abort()
            result = Move.Result()
            result.outcome = "NO_ROUTE"
            return result

        result_future = nav_handle.get_result_async()
        result_done = threading.Event()
        result_future.add_done_callback(lambda _f: result_done.set())
        result_done.wait()
        status = result_future.result().status

        result = Move.Result()
        result.distancia = float(track["dist"])
        result.x = float(track["x"])
        result.y = float(track["y"])
        result.z = float(track["z"])
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Nav2 llegó al destino')
            result.outcome = "REACHED"
            goal_handle.succeed()
        else:
            self.get_logger().warn(
                f'Nav2 no alcanzó el destino (status={status})',
                throttle_duration_sec=5.0)
            result.outcome = "NOT_REACHED"
            goal_handle.abort()
        return result


def main():
    rclpy.init()
    nodo = RobotMovement()
    executor = MultiThreadedExecutor()
    executor.add_node(nodo)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        executor.shutdown()
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
