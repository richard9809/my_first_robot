import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan

class LidarAvoider(Node):

    def __init__(self):
        super().__init__('lidar_avoider')

        # ACT: send driving commands to the robot
        self.publisher_ = self.create_publisher(TwistStamped, 'cmd_vel', 10)

        # SENSE: receive lidar scans
        # qos_profile_sensor_data = "Best Effort", same fix you'd use in RViz
        self.subscription = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, qos_profile_sensor_data
        )

        self.safe_distance = 0.5   # meters: closer than this counts as blocked
        self.forward_speed = 0.15  # m/s (Burger's max is about 0.22)
        self.turn_speed = 0.8      # rad/s
        self.turn_direction = 0    # 0 = not turning, 1 = left, -1 = right
        self.clear_distance = 0.7  # must be this clear before driving forward again

        self.get_logger().info('Lidar avoider started!')

    def sector_min(self, ranges, start_deg, end_deg):
        """Closest valid reading between two angles (0 = straight ahead, CCW positive)."""
        n = len(ranges)
        readings = []
        for deg in range(start_deg, end_deg):
            r = ranges[int((deg % 360) / 360 * n)]
            if math.isfinite(r):           # skip .inf and nan
                readings.append(r)
        return min(readings) if readings else float('inf')

    def scan_callback(self, scan):
        # DECIDE
        front = self.sector_min(scan.ranges, -20, 20)
        left = self.sector_min(scan.ranges, 20, 90)
        right = self.sector_min(scan.ranges, -90, -20)

        message = TwistStamped()
        message.header.stamp = self.get_clock().now().to_msg()

        # Start turning when blocked; stop turning only when well clear
        if self.turn_direction == 0 and front < self.safe_distance:
            self.turn_direction = 1 if left > right else -1
            side = 'left' if self.turn_direction == 1 else 'right'
            self.get_logger().info(f'Obstacle at {front:.2f} m, turning {side}')
        elif self.turn_direction != 0 and front > self.clear_distance:
            self.turn_direction = 0

        if self.turn_direction == 0:
            message.twist.linear.x = self.forward_speed
        else:
            message.twist.angular.z = self.turn_speed * self.turn_direction

        # ACT
        self.publisher_.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = LidarAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()