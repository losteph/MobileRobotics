import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_autonomous_nav = get_package_share_directory('autonomous_nav')

    # 1. Percorsi dei file
    world_file = os.path.join(pkg_autonomous_nav, 'worlds', 'track.sdf')
    urdf_file = os.path.join(pkg_autonomous_nav, 'urdf', 'robot.urdf.xacro')

    # Usa xacro per convertire il file in stringa XML
    robot_desc = ParameterValue(Command(['xacro ', urdf_file]), value_type=str)

    # 2. Avvia Gazebo con la mappa
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    # 3. Nodo Robot State Publisher (Serve a RViz per capire la forma del robot)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}]
    )

    # 4. Inserisce il robot in Gazebo (Legge dal topic ufficiale)
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'my_custom_bot', '-x', '2.0', '-y', '0.75', '-z', '0.2'],
        output='screen'
    )
    # 5. Il Ponte Magico (Fa comunicare i topic di ROS 2 con Gazebo)
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',       # Per muovere il robot
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',    # Per leggere il LiDAR
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',         # Per sapere di quanto si è mosso
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'             # Per il posizionamento 3D
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp_node,
        spawn_node,
        bridge_node
    ])