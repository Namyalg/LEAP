from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    sprayer_health_node = Node(
        package='sprayer_health',
        executable='sprayer_health',
        name='sprayer_health',
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(sprayer_health_node)

    return ld
