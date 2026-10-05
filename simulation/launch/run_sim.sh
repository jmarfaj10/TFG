#!/usr/bin/env bash
# Arranca Gazebo (street_bus.world + TurtleBot3) Y, automaticamente, RViz + Nav2 con tu mapa.
set -e

export TURTLEBOT3_MODEL=${TURTLEBOT3_MODEL:-waffle}

# --- Aislamiento de red (DDS y Gazebo Transport) ---
# Jazzy descubre por defecto TODA la subred (ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET)
# y, sin ROS_DOMAIN_ID, en el dominio 0, que es el que usa todo el mundo. En la red
# de la universidad eso significa ver los nodos de otros: hay varios ros_gz_bridge
# ajenos publicando /clock a la vez. Como aqui todo corre con use_sim_time:=True,
# el tiempo simulado salta entre relojes que no tienen nada que ver, tf2 lo detecta
# ("Detected jump back in time ... Clearing TF buffer") y Gazebo/RViz se quedan
# clavados. Nos encerramos en localhost y en un dominio propio (el 25 es del Go2).
#
# Ojo: se fijan SIN '${VAR:-...}' a proposito. Si la terminal viene de una sesion
# vieja con SUBNET heredado, el ':-' no lo pisa y volvemos al problema.
export ROS_DOMAIN_ID=42
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST

# Gazebo NO usa DDS: gz-transport tiene su propio descubrimiento (multicast en la
# interfaz de red, ZeroMQ por TCP) y le dan igual ROS_DOMAIN_ID y
# ROS_AUTOMATIC_DISCOVERY_RANGE. Sin particion propia, la particion por defecto
# es comun a todos, asi que en la wifi de la facultad nuestros procesos ven los
# Gazebo de otras maquinas y se enganchan a ellos. Sintomas:
#   - 'ros_gz_sim create' pregunta por /gazebo/worlds, la peticion se va al
#     servidor ajeno, caduca a los 5 s y se queda en bucle:
#         [create] Requesting list of world names.   <- cada 5 s, para siempre
#     El robot nunca aparece en el mundo, asi que no hay /odom ni TF odom->base_link
#     y Nav2 escupe sin parar "Invalid frame ID 'odom' ... frame does not exist".
#   - /clock llega de un reloj ajeno y la GUI se queda "not responding".
# GZ_PARTITION filtra en el descubrimiento: solo nos vemos entre nosotros.
# (GZ_IP=127.0.0.1 NO vale: el multicast sigue saliendo por la wifi.)
# Para depurar desde otra terminal ('gz topic -l', 'gz service -l') hay que
# exportar la MISMA particion, o no se vera nada.
export GZ_PARTITION=${GZ_PARTITION:-tfg_$(id -un)}

source /opt/ros/jazzy/setup.bash
# turtlebot3_navigation2 se asume instalado en el sistema (ej. /opt/ros/jazzy)
# source "$HOME/turtlebot3_ws/install/setup.bash"

DOCS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --- Opciones ---
# --force: en vez de abortar, cierra lo que haya corriendo y sigue.
FORCE=0
for arg in "$@"; do
    case "$arg" in
        --force|-f) FORCE=1 ;;
        --help|-h)
            echo "Uso: $(basename "$0") [--force]"
            echo "  --force  cierra simulaciones/Nav2 tuyos que ya esten corriendo"
            exit 0
            ;;
        *) echo ">> Opcion desconocida: $arg" >&2; exit 1 ;;
    esac
done

# --- Comprobacion previa: nada de pilas duplicadas ---
# Dos Nav2 a la vez publican dos action servers 'navigate_to_pose' y los goals
# se rechazan de forma aleatoria. Mejor abortar que depurar eso.
# Solo miramos procesos de ESTE usuario y por nombre exacto de ejecutable: asi no
# nos confunde el contenedor del Go2 (corre como root y en ROS_DOMAIN_ID=25) ni
# cualquier shell que lleve estas palabras en su linea de comando.
# Anclamos con '^' a la ruta del ejecutable: ningun shell empieza su linea de
# comando por /opt/ros, asi que no hay falsos positivos. Nada de pgrep -x aqui:
# compara contra /proc/PID/comm, truncado a 15 caracteres, y
# 'component_container_isolated' tiene 28.
PATRON_CONFLICTO='^(/opt/ros/[^ ]*/lib/(rclcpp_components/component_container_isolated|nav2_[a-z_]*/[a-z_]*|rviz2/rviz2)|gz sim)'

conflictos() {
    pgrep -u "$(id -u)" -f "$PATRON_CONFLICTO" 2>/dev/null | sort -un || true
}

listar_pids() {
    ps -o pid=,cmd= -p "$(echo "$1" | tr '\n' ',' | sed 's/,$//')" >&2
}

CONFLICTOS=$(conflictos)
if [ -n "$CONFLICTOS" ]; then
    echo ">> Ya tienes una simulacion o un Nav2 corriendo:" >&2
    listar_pids "$CONFLICTOS"

    if [ "$FORCE" -eq 0 ]; then
        echo ">> Cierrala antes de volver a lanzar, o repite el comando con --force:" >&2
        echo "     pkill -f 'ros2 launch'; pkill -f 'g[z] sim'; pkill -x rviz2" >&2
        exit 1
    fi

    # Matamos por grupo de procesos, no por PID: asi nos llevamos tambien a los
    # hijos que hayan quedado huerfanos, que es justo lo que queda cuando se
    # cierra la terminal y el cleanup de la sesion anterior no llego a correr.
    echo ">> --force: cerrando la simulacion anterior..."
    MI_PGID=$(ps -o pgid= -p $$ | tr -d ' ')
    PGIDS_VIEJOS=$(
        ps -o pgid= -p "$(echo "$CONFLICTOS" | tr '\n' ',' | sed 's/,$//')" \
            | tr -d ' ' | sort -un | grep -vx "$MI_PGID" || true
    )
    for pgid in $PGIDS_VIEJOS; do
        kill -INT -"$pgid" 2>/dev/null || true
    done
    for _ in 1 2 3 4 5 6 7 8; do
        if [ -z "$(conflictos)" ]; then break; fi
        sleep 1
    done
    # Lo que siga vivo pasados 8s va por las bravas: primero el grupo entero y,
    # por si algun huerfano quedo fuera de esos grupos, tambien por PID.
    if [ -n "$(conflictos)" ]; then
        for pgid in $PGIDS_VIEJOS; do
            kill -9 -"$pgid" 2>/dev/null || true
        done
        sleep 1
        RESTOS=$(conflictos)
        if [ -n "$RESTOS" ]; then
            kill -9 $RESTOS 2>/dev/null || true
            sleep 1
        fi
    fi
    if [ -n "$(conflictos)" ]; then
        echo ">> ERROR: no he conseguido cerrarlo todo:" >&2
        listar_pids "$(conflictos)"
        exit 1
    fi
    echo ">> Limpio."
fi

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
# Cada 'ros2 launch' se arranca con setsid, en su propio grupo de procesos, para
# poder matarlo entero (el y todos sus hijos) sin depender de que se porte bien.
PGIDS=()

lanzar() {
    setsid "$@" &
    PGIDS+=($!)
}

cleanup() {
    trap - EXIT INT TERM HUP
    echo ">> Cerrando simulacion..."
    for pgid in "${PGIDS[@]}"; do
        kill -INT -"$pgid" 2>/dev/null || true
    done
    # Damos margen a que cierren solos; lo que siga vivo va por las bravas.
    for _ in 1 2 3 4 5 6 7 8 9 10; do
        vivos=0
        for pgid in "${PGIDS[@]}"; do
            if kill -0 -"$pgid" 2>/dev/null; then vivos=1; fi
        done
        [ "$vivos" -eq 0 ] && break
        sleep 1
    done
    for pgid in "${PGIDS[@]}"; do
        kill -9 -"$pgid" 2>/dev/null || true
    done
    # Barrido final: 'gz sim' sobrevive a la muerte de su grupo mas veces de las
    # que deberia (el wrapper 'sh -c ruby ... gz sim' muere y el hijo real queda
    # reparentado a init). Un servidor huerfano no se ve, pero se queda con el
    # mundo: en el siguiente lanzamiento hay dos servidores, 'ros_gz_sim create'
    # no consigue la lista de mundos y el robot no llega a aparecer.
    RESTOS=$(conflictos)
    if [ -n "$RESTOS" ]; then
        kill -9 $RESTOS 2>/dev/null || true
    fi
    echo ">> Cerrado."
}
trap cleanup EXIT INT TERM HUP

echo ">> Lanzando Gazebo con el mundo street_bus..."
lanzar ros2 launch "$DOCS/launch/street_bus.launch.py" \
    x_pose:="$X" y_pose:="$Y" yaw_pose:="$YAW_RAD"

echo ">> Esperando a que Gazebo arranque..."
sleep 10

echo ">> Lanzando RViz + Nav2 con el mapa street..."
lanzar ros2 launch nav2_bringup bringup_launch.py \
    use_sim_time:=True map:="$DOCS/maps/street.yaml" \
    params_file:="$DOCS/params/nav2_street.yaml"

echo ">> Abriendo RViz2..."
lanzar ros2 launch nav2_bringup rviz_launch.py

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
