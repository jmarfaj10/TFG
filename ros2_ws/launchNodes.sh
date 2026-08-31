#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if test -d "$DIR/src"; then
    cd "$DIR"
    if colcon build --symlink-install; then
        source install/setup.bash
        CONFIG=$(mktemp)
        WS_DIR=$(pwd)
cat > "$CONFIG" << EOF
[layouts]
  [[ros2nodes]]
    [[[window0]]]
      type = Window
      parent = ""
    [[[vpaned0]]]
      type = VPaned
      parent = window0
    [[[hpaned0]]]
      type = HPaned
      parent = vpaned0
    [[[hpaned1]]]
      type = HPaned
      parent = vpaned0
    [[[terminal1]]]
      type = Terminal
      parent = hpaned0
      command = bash -c "source $WS_DIR/install/setup.bash; echo '[CHAT]'; ros2 run userCommunication userCommunication; exec bash"
    [[[terminal2]]]
      type = Terminal
      parent = hpaned0
      command = bash -c "source $WS_DIR/install/setup.bash; echo '[VLM]'; ros2 run VLMProcessing VLMProcessing; exec bash"
    [[[terminal3]]]
      type = Terminal
      parent = hpaned1
      command = bash -c "source $WS_DIR/install/setup.bash; echo '[COMMUNICATION]'; ros2 run robotCommunication robotCommunication; exec bash"
    [[[hpaned2]]]
      type = HPaned
      parent = hpaned1
    [[[terminal4]]]
      type = Terminal
      parent = hpaned2
      command = bash -c "source $WS_DIR/install/setup.bash; echo '[MOVEMENT]'; ros2 run robotMovement robotMovement; exec bash"
    [[[terminal5]]]
      type = Terminal
      parent = hpaned2
      command = bash -c "source $WS_DIR/install/setup.bash; echo '[WEBSOCKET]'; ros2 run robotWebSocket robotWebSocket; exec bash"
EOF

        terminator -u -g "$CONFIG" -l ros2nodes
        rm -f "$CONFIG"
    else
        echo "La compilación falló, no se abren los paneles"
    fi
else
    echo "No existe el directorio src en $DIR (¿es este la raíz del workspace?)"
fi