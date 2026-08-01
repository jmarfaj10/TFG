import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/upo/Documents/TFG/TFG/ros2_ws/src/install/userCommunication'
