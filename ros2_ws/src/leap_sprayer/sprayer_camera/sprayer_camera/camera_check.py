"""Debug check for the sprayer camera.

Listens to the three topics the sprayer pipeline reads and, every 2 s, prints
what arrived: frame rate, image size, depth at the image centre, lens numbers.
Publishes nothing. Run by hand while SPRAYER is up:

    ros2 run sprayer_camera camera_check
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image

REPORT_PERIOD = 2.0  # seconds


class CameraCheck(Node):
    def __init__(self):
        super().__init__('camera_check')
        self.color = None
        self.depth = None
        self.info = None
        self.color_count = 0
        self.depth_count = 0

        self.create_subscription(Image, '/camera/color/image', self.on_color, qos_profile_sensor_data)
        self.create_subscription(Image, '/camera/depth/image', self.on_depth, qos_profile_sensor_data)
        self.create_subscription(CameraInfo, '/camera/cam_info', self.on_info, qos_profile_sensor_data)
        self.create_timer(REPORT_PERIOD, self.report)

    def on_color(self, msg):
        self.color = msg
        self.color_count += 1

    def on_depth(self, msg):
        self.depth = msg
        self.depth_count += 1

    def on_info(self, msg):
        self.info = msg

    def report(self):
        color_hz = self.color_count / REPORT_PERIOD
        depth_hz = self.depth_count / REPORT_PERIOD
        self.color_count = 0
        self.depth_count = 0

        if color_hz == 0 and depth_hz == 0:
            self.get_logger().warn('no images on /camera/color/image or /camera/depth/image')
            return

        lines = []
        if self.color is not None:
            c = self.color
            lines.append(f'color {color_hz:4.1f} Hz  {c.width}x{c.height} {c.encoding}')
        if self.depth is not None:
            d = self.depth
            lines.append(f'depth {depth_hz:4.1f} Hz  {d.width}x{d.height} {d.encoding}'
                         f'  centre {centre_depth_m(d)}')
        if self.color is not None and self.depth is not None:
            gap_ms = abs(stamp_s(self.color) - stamp_s(self.depth)) * 1000.0
            lines.append(f'color/depth stamp gap {gap_ms:.1f} ms')
        if self.info is not None:
            k = self.info.k
            lines.append(f'cam_info fx={k[0]:.1f} fy={k[4]:.1f} cx={k[2]:.1f} cy={k[5]:.1f}'
                         f'  frame={self.info.header.frame_id}')
        else:
            lines.append('no /camera/cam_info yet')
        self.get_logger().info('\n  '.join([''] + lines))


def stamp_s(msg):
    return msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9


def centre_depth_m(msg):
    """Depth at the centre pixel of a 16UC1 image (millimetres) as a string in metres."""
    if msg.encoding != '16UC1':
        return f'(not 16UC1: {msg.encoding})'
    i = (msg.height // 2) * msg.step + (msg.width // 2) * 2
    order = 'big' if msg.is_bigendian else 'little'
    mm = int.from_bytes(bytes(msg.data[i:i + 2]), order)
    return 'no reading (0)' if mm == 0 else f'{mm / 1000.0:.3f} m'


def main(args=None):
    rclpy.init(args=args)
    node = CameraCheck()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
