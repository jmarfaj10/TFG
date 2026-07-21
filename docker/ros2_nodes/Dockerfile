# ─── Nodos ROS2 (Jazzy) — se despliega en el ROBOT ───────────────────
# Contexto de build = raíz del repo (~/TFG), así este Dockerfile puede
# copiar tanto ros2_ws/ como los ficheros de ayuda de docker/ros2_nodes/.
FROM ros:jazzy

# Dependencias de sistema que NO están declaradas en los package.xml
# (los nodos hacen import cv2 / numpy / requests directamente) + colcon.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-colcon-common-extensions \
        python3-opencv \
        python3-numpy \
        python3-requests \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws

# Código fuente del workspace (incluye src/config.yaml que usan los setup.py)
COPY ros2_ws/src ./src

# Resolvemos e instalamos las dependencias declaradas en los package.xml
# (rclpy, cv_bridge, tf2, nav2_msgs, message_filters, geometry_msgs, ...)
RUN . /opt/ros/jazzy/setup.sh \
    && apt-get update \
    && (rosdep init 2>/dev/null || true) \
    && rosdep update --rosdistro jazzy \
    && rosdep install --from-paths src --ignore-src -r -y \
    && rm -rf /var/lib/apt/lists/*

# Compilamos el workspace (interfaces + los 4 paquetes de nodos)
RUN . /opt/ros/jazzy/setup.sh \
    && colcon build --symlink-install

# Launch que arranca los 4 nodos y entrypoint que sourcea ROS2 + workspace
COPY docker/ros2_nodes/bringup.launch.py /root/bringup.launch.py
COPY docker/ros2_nodes/ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]
# USE_SIM_TIME lo inyecta el compose (false=robot real, true=simulación)
CMD ["bash", "-c", "ros2 launch /root/bringup.launch.py use_sim_time:=${USE_SIM_TIME:-false}"]
