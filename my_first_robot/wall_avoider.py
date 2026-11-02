import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class WallAvoider(Node):

    def __init__(self):
        super().__init__('wall_avoider')

        # ACT: send movement commands
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        # SENSE: receive the turtle's position whenever it changes
        self.subscription = self.create_subscription(
            Pose, 'turtle1/pose', self.pose_callback, 10
        )

        self.center = 5.5   # middle of the turtlesim world
        self.margin = 1.5   # how close to a wall counts as "too close"

        self.get_logger().info('Wall avoider started!')

    def pose_callback(self, pose):
        # DECIDE: runs every time a new position arrives
        message = Twist()

        near_wall = (
            pose.x < self.margin or pose.x > 11.0 - self.margin or
            pose.y < self.margin or pose.y > 11.0 - self.margin
        )

        if not near_wall:
            message.linear.x = 2.0  # open space: drive straight
        else:
            # Which direction is the center, from where the turtle is now?
            angle_to_center = math.atan2(self.center - pose.y,
                                         self.center - pose.x)
            # How far off is the turtle's heading from that direction?
            error = angle_to_center - pose.theta
            error = math.atan2(math.sin(error), math.cos(error))  # keep it between -pi and pi

            if abs(error) > 0.2:
                message.angular.z = 2.0 if error > 0 else -2.0  # turn toward center
            else:
                message.linear.x = 2.0  # facing center: drive away from wall

        self.publisher_.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = WallAvoider()
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