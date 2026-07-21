#!/bin/bash
set -e

# Entorno base de ROS2
source /opt/ros/jazzy/setup.bash

# Tu workspace ya compilado
if [ -f /ros2_ws/install/setup.bash ]; then
  source /ros2_ws/install/setup.bash
fi

exec "$@"
