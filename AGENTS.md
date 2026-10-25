# ROS 2 Launch File Coding Guidelines

## Scope
These rules apply to all ROS 2 Python launch files (`*.launch.py`) in this repository.

## Main goal
Write clean, flat, readable launch files that a ROS 2 developer can understand and modify quickly. Prefer straightforward, explicit code over clever abstractions.

## Structure
- Use `generate_launch_description()` as the main entry point.
- Organize code in this order: imports, package paths and constants, launch arguments, launch configurations, node/include definitions, and `LaunchDescription` return.
- Keep each `Node`, `IncludeLaunchDescription`, and `DeclareLaunchArgument` in a clearly named variable when this improves readability.
- Return a simple, ordered `LaunchDescription([...])` list.
- Use descriptive snake_case names such as `robot_state_publisher_node` and `controller_spawner`.
- Group related arguments, parameters, remappings, and conditions on separate lines.

## Simplicity rules
- Avoid nested expressions, deeply nested constructors, and one-line conditional tricks.
- Do not use `OpaqueFunction`, `PythonExpression`, `lambda`, dynamic introspection, or custom launch helpers unless the requirement cannot be met cleanly with standard launch APIs.
- Do not introduce helper functions or classes for one-off operations.
- Do not introduce `GroupAction`, `PushRosNamespace`, or event handlers unless they are needed for correct behavior.
- Prefer simple explicit code even if it takes a few more lines.
- Avoid unnecessary variables, imports, comments, and layers of indirection.
- Never trade correctness for brevity.

## Paths and substitutions
- Use `get_package_share_directory()` and `os.path.join()` for paths fully resolvable in ordinary Python.
- Use `FindPackageShare` and `PathJoinSubstitution` when path components depend on launch-time substitutions.
- Store complex substitution objects in named variables rather than nesting them inside `Node` or `IncludeLaunchDescription` calls.
- Use `LaunchConfiguration` for values supplied by launch arguments.
- Use `ParameterValue(..., value_type=...)` or `LaunchConfigAsBool` where explicit type handling is necessary and supported by the ROS 2 distribution.
- Avoid `PythonExpression` for boolean conditions; prefer `IfCondition` and `UnlessCondition` when sufficient.

## Nodes and namespaces
- Make node names, namespaces, parameters, remappings, and output settings easy to inspect.
- For multi-robot launches, keep namespaces explicit and consistent.
- Use relative topic names when namespacing is intended; do not silently introduce leading `/`.
- Keep frame IDs, TF remappings, controller manager paths, and topic names consistent with the actual robot configuration.
- Do not assume that a ROS namespace automatically prefixes TF frame IDs.
- Avoid global remappings or namespace changes that may affect unrelated nodes.

## Includes and controllers
- Keep `IncludeLaunchDescription` arguments explicit and readable.
- Use separate named variables for included launch files and their argument dictionaries when useful.
- For controller spawners, use the correct namespaced controller manager path.
- Add startup ordering or event handlers only when required; explain the dependency briefly.
- Do not change controller lifecycle or startup sequencing while refactoring for style.

## Comments and formatting
- Follow PEP 8 with four-space indentation.
- Prefer a maximum line length around 88-100 characters.
- Use short comments to explain non-obvious behavior, not obvious syntax.
- Avoid excessive banners, decorative separators, and redundant comments.
- Keep import groups clean and remove unused imports.

## Refactoring safety
- Preserve runtime behavior unless the task explicitly requests a change.
- Do not silently change package names, executable names, launch argument names, defaults, topic remappings, namespaces, TF frame IDs, controller names, or parameters.
- Prefer minimal diffs over rewriting an entire launch file.
- If a simpler form would change semantics, keep the correct form and explain why.
- Do not invent package or executable names: inspect the repository first.

## Validation
- Check Python syntax with `python3 -m py_compile <launch_file>`.
- When ROS 2 is available, run `ros2 launch <package> <file.launch.py> --show-args` to inspect arguments.
- Run launch-time or runtime tests only when dependencies and hardware/simulation conditions allow.
- Report what was validated and what could not be tested.

## Preferred example
```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    description_share = get_package_share_directory("my_robot_description")
    config_file = os.path.join(description_share, "config", "robot.yaml")

    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="robot1",
        description="Robot namespace",
    )

    namespace = LaunchConfiguration("namespace")

    robot_node = Node(
        package="my_robot_driver",
        executable="driver_node",
        namespace=namespace,
        name="driver",
        parameters=[config_file],
        remappings=[
            ("cmd_vel", "cmd_vel"),
        ],
        output="screen",
    )

    return LaunchDescription([
        namespace_arg,
        robot_node,
    ])
```

The example illustrates style only. Never assume its placeholder packages exist in the actual workspace.
