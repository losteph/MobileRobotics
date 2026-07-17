import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Trova in automatico dove si trova il TUO pacchetto
    my_pkg_path = get_package_share_directory('autonomous_nav')
    
    # 2. Punta direttamente al tuo file URDF
    my_urdf_file = os.path.join(my_pkg_path, 'urdf', 'robot.xacro')
    
    # 3. Usa il tool ufficiale di ROS per far apparire RViz e gli slider
    urdf_tutorial_path = get_package_share_directory('urdf_tutorial')
    
    display_tool = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(urdf_tutorial_path, 'launch', 'display.launch.py')),
        launch_arguments={'model': my_urdf_file}.items()
    )

    return LaunchDescription([
        display_tool
    ])