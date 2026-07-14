import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import userCommunication.constants as constants

# --- AUDIO (speech-to-text) -------------------------------------------------
# Parte de audio dejada preparada pero comentada. Para activarla:
#   1) Instala las dependencias:  pip install SpeechRecognition pyaudio
#   2) Descomenta el bloque de import de abajo.
#   3) Descomenta el método _audio_loop y su uso en _input_loop.
#
# try:
#     import speech_recognition as sr
#     AUDIO_AVAILABLE = True
# except ImportError:
#     AUDIO_AVAILABLE = False
# ----------------------------------------------------------------------------


class UserCommunication(Node):
    """Nodo que recoge peticiones del usuario (teclado o voz) y las publica
    en el canal que escucha el robot."""

    def __init__(self):
        super().__init__('userCommunication')

        # Parámetro para elegir el modo de entrada: 'keyboard' o 'audio'.
        self.declare_parameter('input_mode', 'keyboard')
        self.input_mode = self.get_parameter('input_mode').value

        self.pub_user = self.create_publisher(String, constants.USER_CHANNEL_COMM, 10)

        # Respuesta en texto del VLM (canal propio de respuestas, distinto del
        # canal de peticiones, para no recibir de vuelta lo que enviamos).
        self.sub_resp = self.create_subscription(
            String, constants.RESPONSE_CHANNEL_VLM, self._on_response, 10)

        # El bucle de entrada (input()/micrófono) es bloqueante, así que va en
        # un hilo aparte para no bloquear el spin de ROS.
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._input_loop, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------ #
    # Publicación
    # ------------------------------------------------------------------ #
    def publish_message(self, text):
        text = (text or '').strip()
        if not text:
            return
        msg = String()
        msg.data = text
        self.pub_user.publish(msg)
        self.get_logger().info(f'Petición enviada: "{text}"')

    # ------------------------------------------------------------------ #
    # Recepción de la respuesta del VLM
    # ------------------------------------------------------------------ #
    def _on_response(self, msg):
        # \r + salto de línea para no pisar el prompt "> " del input()
        print(f'\n🤖 {msg.data}\n> ', end='', flush=True)

    # ------------------------------------------------------------------ #
    # Bucle de entrada
    # ------------------------------------------------------------------ #
    def _input_loop(self):
        # if self.input_mode == 'audio':
        #     self._audio_loop()
        # else:
        #     self._keyboard_loop()
        self._keyboard_loop()

    def _keyboard_loop(self):
        self.get_logger().info(
            'Modo teclado. Escribe tu petición y pulsa Enter '
            '(escribe "salir" para terminar).')
        while not self._stop.is_set():
            try:
                text = input('> ')
            except (EOFError, KeyboardInterrupt):
                break
            if text.strip().lower() in ('salir', 'exit', 'quit'):
                break
            self.publish_message(text)

    # ------------------------------------------------------------------ #
    # Bucle de audio (preparado, comentado)
    # ------------------------------------------------------------------ #
    # def _audio_loop(self):
    #     if not AUDIO_AVAILABLE:
    #         self.get_logger().error(
    #             'Modo audio solicitado pero falta SpeechRecognition. '
    #             'Instálalo con: pip install SpeechRecognition pyaudio. '
    #             'Cambiando a modo teclado.')
    #         self._keyboard_loop()
    #         return
    #
    #     recognizer = sr.Recognizer()
    #     mic = sr.Microphone()
    #     with mic as source:
    #         recognizer.adjust_for_ambient_noise(source)
    #     self.get_logger().info('Modo audio. Habla cuando quieras...')
    #
    #     while not self._stop.is_set():
    #         try:
    #             with mic as source:
    #                 audio = recognizer.listen(source, phrase_time_limit=10)
    #             # Reconocedor de Google (online). Sustituible por un backend
    #             # offline (Vosk, Whisper, etc.) si se prefiere.
    #             text = recognizer.recognize_google(audio, language='es-ES')
    #             self.publish_message(text)
    #         except sr.UnknownValueError:
    #             self.get_logger().warn('No se entendió el audio.')
    #         except sr.RequestError as exc:
    #             self.get_logger().error(f'Error del servicio de voz: {exc}')
    #         except Exception as exc:  # noqa: BLE001
    #             self.get_logger().error(f'Error capturando audio: {exc}')

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