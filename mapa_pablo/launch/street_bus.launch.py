#!/usr/bin/env python3
# Lanza el mundo street_bus.world en Gazebo Sim (Harmonic) con el TurtleBot3.
# Reutiliza el spawn + ros_gz_bridge del paquete turtlebot3_gazebo.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


# Carpeta Documents (donde viven /models, /world, /maps)
DOCS = os.path.expanduser('~/Documents')


def generate_launch_description():
    tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    launch_file_dir = os.path.join(tb3_gazebo, 'launch')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # Pose de aparicion del robot (dentro del mapa 50x50 centrado en 0)
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    z_pose = LaunchConfiguration('z_pose', default='0.08')  # cara superior del suelo (floor) esta en z=0.05
    yaw_pose = LaunchConfiguration('yaw_pose', default='0.0')  # radianes

    world = os.path.join(DOCS, 'world', 'street_bus.world')

    # Rutas donde Gazebo busca los modelos referenciados con model://
    set_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.pathsep.join([
            os.path.join(DOCS, 'models'),                       # bus_stop
            os.path.join(tb3_gazebo, 'models'),                 # turtlebot3_waffle, etc.
            os.path.join(
                get_package_share_directory('ros_gz_sim_demos'),
                'models'),                                      # cardboard_box
        ]),
    )

    # Servidor de Gazebo (-r arranca la simulacion, -s solo servidor)
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -s -v2 ', world],
                          'on_exit_shutdown': 'true'}.items(),
    )

    # Cliente (GUI) de Gazebo
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-g -v2 ',
                          'on_exit_shutdown': 'true'}.items(),
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    # Spawn del robot con pose (x, y, yaw). No usamos spawn_turtlebot3.launch.py
    # porque ese ignora la orientacion; aqui la pasamos con -Y para que Gazebo y
    # la pose inicial de RViz/Nav2 coincidan.
    turtlebot3_model = os.environ['TURTLEBOT3_MODEL']
    model_folder = 'turtlebot3_' + turtlebot3_model
    urdf_path = os.path.join(tb3_gazebo, 'models', model_folder, 'model.sdf')

    spawn_turtlebot_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', turtlebot3_model,
            '-file', urdf_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose,
            '-Y', yaw_pose,
        ],
        output='screen',
    )

    # Bridges ROS <-> Gazebo (cmd_vel, scan, odom, tf, imu...)
    bridge_params = os.path.join(
        tb3_gazebo, 'params', model_folder + '_bridge.yaml')

    gz_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    gz_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw', '/camera/depth_image'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    ld = LaunchDescription()
    ld.add_action(set_resource_path)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(spawn_turtlebot_cmd)
    ld.add_action(gz_bridge_cmd)
    if turtlebot3_model != 'burger':
        ld.add_action(gz_image_bridge_cmd)
    ld.add_action(robot_state_publisher_cmd)
    return ld
