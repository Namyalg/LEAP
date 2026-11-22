"""
sprayer_health.py

Health/status node for the sprayer stack on the Amiga. It is started by the
SPRAYER entry in the field panel (launch.py) through
leap_launch/amiga_sprayer.launch.py.

For now it only reports that the sprayer stack is up: it publishes
std_msgs/String "standby" on /sprayer/status once a second. It does not
connect to the camera, the Arduino, the pump or the nozzles.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SprayerHealth(Node):
    def __init__(self):
        super().__init__('sprayer_health')

        self.status_pub = self.create_publisher(String, '/sprayer/status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('sprayer_health started (no hardware connected)')

    def publish_status(self):
        msg = String()
        msg.data = 'standby'
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SprayerHealth()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
