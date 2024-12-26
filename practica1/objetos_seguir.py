import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist


MAX_RANGE = 0.15


class objetosSeguir(Node):
    def __init__(self):
        super().__init__('objetos_seguir')

        self.__publisher = self.create_publisher(Twist, 'cmd_vel', 1)

        self.create_subscription(Range, 'ps7', self.__left_sensor_callback, 1)
        self.create_subscription(Range, 'ps0', self.__right_sensor_callback, 1)

    def __left_sensor_callback(self, message):
        self.__left_sensor_value = message.range

    def __right_sensor_callback(self, message):
        self.__right_sensor_value = message.range

        command_message = Twist()

        command_message.linear.x = 0.1
        #cuanto mas cerca, mas bajo
        if self.__left_sensor_value < self.__right_sensor_value:
            command_message.angular.z = 0.6
        else:
            command_message.angular.z = -0.6

        self.__publisher.publish(command_message)


def main(args=None):
    rclpy.init(args=args)
    seguir = objetosSeguir()
    rclpy.spin(seguir)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    seguir.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
