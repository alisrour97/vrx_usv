import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class DynamicPositioningNode(Node):

    def __init__(self):
        super().__init__('dynamic_positioning_node')

        # Create publishers
        self.pos_publisher = self.create_publisher(Float64, '/wamv/thrusters/right/pos', 10)
        self.thrust_publisher = self.create_publisher(Float64, '/wamv/thrusters/right/thrust', 10)

        # Timer to publish data periodically
        self.timer = self.create_timer(0.5, self.publish_data)

        # Initialize values
        self.pos_value = 0.0
        self.thrust_value = 0.0

    def publish_data(self):
        # Create and publish position message
        pos_msg = Float64()
        pos_msg.data = self.pos_value
        self.pos_publisher.publish(pos_msg)
        self.get_logger().info(f'Published position: {self.pos_value}')

        # Create and publish thrust message
        thrust_msg = Float64()
        thrust_msg.data = self.thrust_value
        self.thrust_publisher.publish(thrust_msg)
        self.get_logger().info(f'Published thrust: {self.thrust_value}')

        # Update values (example logic for testing)
        self.pos_value += 0.1
        self.thrust_value += 1.0

def main(args=None):
    rclpy.init(args=args)
    node = DynamicPositioningNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()