import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    bringup_package_path = get_package_share_directory('bringup')
    default_params_file = os.path.join(
        bringup_package_path, 'config', 'load_map.yaml'
    )

    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace for map nodes; the map topic remains global /map.',
    )
    map_name_arg = DeclareLaunchArgument(
        'map_name',
        default_value='room',
        description='Map folder under bringup/maps containing map.yaml and its image.',
    )
    map_arg = DeclareLaunchArgument(
        'map',
        default_value=PathJoinSubstitution([
            bringup_package_path, 'maps', LaunchConfiguration('map_name'), 'map.yaml'
        ]),
        description='Map YAML path; overrides the path selected by map_name.',
    )
    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=default_params_file,
        description='Map server and lifecycle manager parameters file.',
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use the simulation clock.',
    )
    autostart_arg = DeclareLaunchArgument(
        'autostart',
        default_value='true',
        description='Automatically configure and activate map_server.',
    )
    map_frame_arg = DeclareLaunchArgument(
        'map_frame',
        default_value='map',
        description='Global map frame; must match the AMCL map_frame argument.',
    )

    namespace = LaunchConfiguration('namespace')
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    map_frame = LaunchConfiguration('map_frame')

    map_params = RewrittenYaml(
        source_file=params_file,
        root_key=namespace,
        param_rewrites={
            'use_sim_time': use_sim_time,
            'autostart': autostart,
            'yaml_filename': map_yaml_file,
            'frame_id': map_frame,
            'topic_name': '/map',
        },
        convert_types=True,
    )

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        namespace=namespace,
        parameters=[map_params],
        output='screen',
    )
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        namespace=namespace,
        parameters=[map_params],
        output='screen',
    )

    return LaunchDescription([
        namespace_arg,
        map_name_arg,
        map_arg,
        params_file_arg,
        use_sim_time_arg,
        autostart_arg,
        map_frame_arg,
        map_server_node,
        lifecycle_manager_node,
    ])
