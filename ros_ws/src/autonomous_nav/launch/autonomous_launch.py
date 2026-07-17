import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_autonomous_nav = get_package_share_directory('autonomous_nav')

    # 1. Chiama il file di simulazione base (Mappa + Robot + Bridge)
    simulation_base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_autonomous_nav, 'launch', 'simulation_launch.py')
        )
    )

    # 2. Avvia il Nodo di Percezione
    perception_node = Node(
        package='autonomous_nav',
        executable='perception',
        name='perception_node',
        output='screen'
    )

    # 3. Avvia il Nodo di Controllo
    control_node = Node(
        package='autonomous_nav',
        executable='controller',
        name='control_node',
        output='screen'
    )

    return LaunchDescription([
        simulation_base,
        perception_node,
        control_node
    ])