import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    bringup_package_path = get_package_share_directory('bringup')
    default_params_file = os.path.join(
        bringup_package_path, 'config', 'localization.yaml'
    )

    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace for AMCL, its lifecycle manager and scan topic.',
    )
    frame_prefix_arg = DeclareLaunchArgument(
        'frame_prefix',
        default_value='',
        description='Prefix for odom and base frames, including a trailing slash (robot1/).',
    )
    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=default_params_file,
        description='Localization parameters file.',
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use the simulation clock.',
    )
    autostart_arg = DeclareLaunchArgument(
        'autostart',
        default_value='true',
        description='Automatically configure and activate amcl.',
    )
    map_frame_arg = DeclareLaunchArgument(
        'map_frame',
        default_value='map',
        description='Global map frame shared by the robots; not prefixed automatically.',
    )
    scan_topic_arg = DeclareLaunchArgument(
        'scan_topic',
        default_value='scan',
        description='LaserScan topic, relative to namespace unless absolute.',
    )

    namespace = LaunchConfiguration('namespace')
    frame_prefix = LaunchConfiguration('frame_prefix')
    params_file = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    map_frame = LaunchConfiguration('map_frame')
    scan_topic = LaunchConfiguration('scan_topic')

    localization_params = RewrittenYaml(
        source_file=params_file,
        root_key=namespace,
        param_rewrites={
            'use_sim_time': use_sim_time,
            'autostart': autostart,
            'global_frame_id': map_frame,
            'odom_frame_id': [frame_prefix, 'odom'],
            'base_frame_id': [frame_prefix, 'base_footprint'],
            'scan_topic': scan_topic,
        },
        convert_types=True,
    )

    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        namespace=namespace,
        parameters=[localization_params],
        remappings=[
            ('map', '/map'),
            ('/tf', '/tf'),
            ('/tf_static', '/tf_static'),
        ],
        output='screen',
    )
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        namespace=namespace,
        parameters=[localization_params],
        output='screen',
    )

    return LaunchDescription([
        namespace_arg,
        frame_prefix_arg,
        params_file_arg,
        use_sim_time_arg,
        autostart_arg,
        map_frame_arg,
        scan_topic_arg,
        amcl_node,
        lifecycle_manager_node,
    ])
