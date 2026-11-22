from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    sprayer_control_node = Node(
        package='leap_sprayer',
        executable='sprayer_control',
        name='sprayer_control',
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(sprayer_control_node)

    return ld
