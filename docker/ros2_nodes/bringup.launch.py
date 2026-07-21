# Arranca los 4 nodos del TFG en un solo proceso (equivalente a los 4
# paneles de terminator de launchNodes.sh, pero sin GUI).
#
# use_sim_time:
#   false (por defecto) -> robot real (usa el reloj del sistema)
#   true                -> simulación en Gazebo (usa el /clock del simulador)
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    params = [{'use_sim_time': use_sim_time}]

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='true en simulación (Gazebo), false en robot real'),

        Node(package='userCommunication', executable='userCommunication',
             name='userCommunication', output='screen', parameters=params),
        Node(package='VLMProcessing', executable='VLMProcessing',
             name='VLMProcessing', output='screen', parameters=params),
        Node(package='robotCommunication', executable='robotCommunication',
             name='robotCommunication', output='screen', parameters=params),
        Node(package='robotMovement', executable='robotMovement',
             name='robotMovement', output='screen', parameters=params),
    ])
