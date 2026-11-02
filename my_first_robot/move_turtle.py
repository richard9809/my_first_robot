import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleMover(Node):
    def __init__(self):
        super().__init__('turtle_mover')

        self.publisher_ = self.create_publisher(
            Twist, 
            'turtle1/cmd_vel', 
            10
        )

        self.speed = 0.5  # Set the speed of the turtle

        self.timer = self.create_timer(0.5, self.move_turtle)

        self.get_logger().info('Turtle mover started!')

    def move_turtle(self):
        message = Twist()

        message.linear.x = self.speed  # Move forward with a speed of 1.0
        message.angular.z = 0.5 # Rotate with an angular speed of 2.0

        self.publisher_.publish(message)
        self.speed += 0.05  # Increase the speed for the next iteration

def main(args=None):
    rclpy.init(args=args)   # start the ROS 2 Python client library

    node = TurtleMover()

    try:
        rclpy.spin(node)    # keep the node alive, running its timers, until Ctrl+C  
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node() # clean up the node before shutting down
        rclpy.shutdown()


if __name__ == '__main__':
    main()