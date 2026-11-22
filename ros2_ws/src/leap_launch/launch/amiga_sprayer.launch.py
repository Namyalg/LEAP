import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    sprayer_health_node = Node(
        package='sprayer_health',
        executable='sprayer_health',
        name='sprayer_health',
        output='screen'
    )

    # Sprayer frames (boom, nozzles, camera mount) relative to sprayer_base, from
    # its URDF. Own node name and description topic, so it doesn't clash with
    # LEAP's robot_state_publisher (started by SENSORS) or its /robot_description.
    sprayer_urdf = os.path.join(
        get_package_share_directory('sprayer_description'), 'urdf', 'sprayer.urdf.xacro'
    )
    sprayer_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='sprayer_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(
                Command([FindExecutable(name='xacro'), ' ', sprayer_urdf]),
                value_type=str
            )
        }],
        remappings=[('robot_description', '/sprayer/robot_description')]
    )

    ld = LaunchDescription()
    ld.add_action(sprayer_health_node)
    ld.add_action(sprayer_state_publisher)

    return ld
