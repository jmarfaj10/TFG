#!/usr/bin/env bash
# Arranca Gazebo (street_bus.world + TurtleBot3) Y, automaticamente, RViz + Nav2 con tu mapa.
set -e

export TURTLEBOT3_MODEL=${TURTLEBOT3_MODEL:-waffle}
source /opt/ros/jazzy/setup.bash
# turtlebot3_navigation2 vive en el workspace, no en /opt/ros: hay que sourcearlo.
source "$HOME/turtlebot3_ws/install/setup.bash"

DOCS="$HOME/Documents"

# --- Pose inicial del robot (se usa en Gazebo y en RViz/Nav2) ---
read -p ">> Coordenada X [0.0]: " X;        X=${X:-0.0}
read -p ">> Coordenada Y [0.0]: " Y;        Y=${Y:-0.0}
read -p ">> Orientacion yaw en grados [0]: " YAW_DEG; YAW_DEG=${YAW_DEG:-0.0}

# Convertimos yaw a radianes (Gazebo) y a cuaternion (initialpose de Nav2).
read YAW_RAD QZ QW < <(python3 -c "import math,sys
d=math.radians(float('$YAW_DEG'))
print(d, math.sin(d/2), math.cos(d/2))")

echo ">> Pose elegida: x=$X y=$Y yaw=${YAW_DEG}deg"

# Al salir (Ctrl+C) matamos tambien Gazebo y todo lo lanzado en segundo plano.
cleanup() {
    echo ">> Cerrando simulacion..."
    kill 0
}
trap cleanup EXIT INT TERM

echo ">> Lanzando Gazebo con el mundo street_bus..."
ros2 launch "$DOCS/launch/street_bus.launch.py" \
    x_pose:="$X" y_pose:="$Y" yaw_pose:="$YAW_RAD" &

echo ">> Esperando a que Gazebo arranque..."
sleep 10

echo ">> Lanzando RViz + Nav2 con el mapa street..."
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
    use_sim_time:=True map:="$DOCS/maps/street.yaml" \
    params_file:="$DOCS/params/nav2_street.yaml" &

echo ">> Esperando a que Nav2/AMCL arranque..."
sleep 12

# Publicamos la pose inicial para que AMCL/RViz situen el robot donde toca.
# Repetimos por si AMCL aun no se ha suscrito al primer intento.
echo ">> Fijando pose inicial en RViz/Nav2..."
for i in 1 2 3; do
    ros2 topic pub --once /initialpose \
        geometry_msgs/msg/PoseWithCovarianceStamped \
        "{header: {frame_id: 'map'}, pose: {pose: {position: {x: $X, y: $Y, z: 0.0}, orientation: {z: $QZ, w: $QW}}}}"
    sleep 1
done

echo ">> Listo. Ctrl+C para cerrar todo."
wait
