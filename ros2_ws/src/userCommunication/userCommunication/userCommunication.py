import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import userCommunication.constants as constants
import json


class UserCommunication(Node):

    def __init__(self):
        super().__init__('userCommunication')

        self.pub_user = self.create_publisher(String, constants.USER_CHANNEL_COMM, 10)

        self.sub_resp = self.create_subscription(
            String, constants.RESPONSE_CHANNEL_VLM, self._on_response, 10)

        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._keyboard_loop, daemon=True)
        self._thread.start()


    def publish_message(self, text):
        text = (text or '').strip()
        if not text:
            return
        msg = String()
        msg.data = text
        self.pub_user.publish(msg)


    def _on_response(self, msg):
        try:
            texto = json.loads(msg.data).get("data", msg.data)
        except (json.JSONDecodeError, TypeError):
            texto = msg.data
        print(f'\n🤖 {texto}\n> ', end='', flush=True)


    def _keyboard_loop(self):
        while not self._stop.is_set():
            try:
                text = input('> ')
            except (EOFError, KeyboardInterrupt):
                break
            if text.strip().lower() == 'exit':
                break
            self.publish_message(text)

    def destroy_node(self):
        self._stop.set()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UserCommunication()
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