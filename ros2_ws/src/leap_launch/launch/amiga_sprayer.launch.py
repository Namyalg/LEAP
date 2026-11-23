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

    # RealSense D435 (Intel's driver), settings from LEAP_sprayer bringup's
    # realsense_config.yaml. publish_tf off: the sprayer URDF already publishes the
    # D435_* frames. Remapped to the topic names the sprayer pipeline reads.
    realsense_camera = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        namespace='camera',
        name='D435',
        output='screen',
        parameters=[{
            'enable_sync': True,
            'align_depth.enable': True,
            'enable_color': True,
            'enable_depth': True,
            'rgb_camera.enable_auto_white_balance': False,
            'rgb_camera.white_balance': 3500.0,
            'publish_tf': False,
        }],
        remappings=[
            ('/camera/D435/color/image_raw', '/camera/color/image'),
            ('/camera/D435/aligned_depth_to_color/image_raw', '/camera/depth/image'),
            ('/camera/D435/aligned_depth_to_color/camera_info', '/camera/cam_info'),
        ]
    )

    ld = LaunchDescription()
    ld.add_action(sprayer_health_node)
    ld.add_action(sprayer_state_publisher)
    ld.add_action(realsense_camera)

    return ld
