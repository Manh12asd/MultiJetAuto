import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    slam_package_path = get_package_share_directory('slam')
    robot_launch_path = os.path.join(
        slam_package_path, 'launch', 'include', 'robot.launch.py'
    )

    sim_arg = DeclareLaunchArgument(
        'sim',
        default_value='true',
        description='Use simulation time and joystick speed limits.',
    )
    master_name_arg = DeclareLaunchArgument(
        'master_name',
        default_value='/',
        description='Robot name used to select the shared map frame.',
    )
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='/',
        description='Robot namespace and TF frame prefix.',
    )
    depth_camera_name_arg = DeclareLaunchArgument(
        'depth_camera_name',
        default_value='depth_cam',
        description='Camera name forwarded to the robot launch.',
    )
    use_joy_arg = DeclareLaunchArgument(
        'use_joy',
        default_value='true',
        description='Enable joystick control.',
    )
    use_depth_camera_arg = DeclareLaunchArgument(
        'use_depth_camera',
        default_value='false',
        description='Disable the LiDAR launch when true; the camera always starts.',
    )
    action_name_arg = DeclareLaunchArgument(
        'action_name',
        default_value='init',
        description='Servo action group used for the initial pose.',
    )

    sim = LaunchConfiguration('sim')
    master_name = LaunchConfiguration('master_name')
    robot_name = LaunchConfiguration('robot_name')
    depth_camera_name = LaunchConfiguration('depth_camera_name')
    use_joy = LaunchConfiguration('use_joy')
    use_depth_camera = LaunchConfiguration('use_depth_camera')
    action_name = LaunchConfiguration('action_name')

    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path),
        launch_arguments={
            'sim': sim,
            'master_name': master_name,
            'robot_name': robot_name,
            'depth_camera_name': depth_camera_name,
            'use_joy': use_joy,
            'use_depth_camera': use_depth_camera,
            'action_name': action_name,
        }.items(),
    )

    return LaunchDescription([
        sim_arg,
        master_name_arg,
        robot_name_arg,
        depth_camera_name_arg,
        use_joy_arg,
        use_depth_camera_arg,
        action_name_arg,
        robot_launch,
    ])
