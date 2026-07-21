# ─── rosbridge — se despliega en el ROBOT ────────────────────────────
# Deja rosbridge-suite ya instalado en la imagen (arranque instantáneo y
# sin depender de internet en el robot, a diferencia del apt-get en runtime).
FROM ros:jazzy

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-jazzy-rosbridge-suite \
    && rm -rf /var/lib/apt/lists/*

# El entrypoint de la imagen base ya hace source de /opt/ros/jazzy
CMD ["ros2", "launch", "rosbridge_server", "rosbridge_websocket_launch.xml"]
