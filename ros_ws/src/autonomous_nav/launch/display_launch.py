import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    my_pkg_path = get_package_share_directory('autonomous_nav')
    
    my_urdf_file = os.path.join(my_pkg_path, 'urdf', 'robot.urdf')
    
    urdf_tutorial_path = get_package_share_directory('urdf_tutorial')
    
    display_tool = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(urdf_tutorial_path, 'launch', 'display.launch.py')),
        launch_arguments={'model': my_urdf_file}.items()
    )

    return LaunchDescription([
        display_tool
    ])
