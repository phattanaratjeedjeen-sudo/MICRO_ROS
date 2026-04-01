#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32
import numpy as np


class DummyNode(Node):
    def __init__(self):
        super().__init__('dummy_node')
        hz = 20
        self.msg = 1
        self.create_timer(1.0 / hz, self.timer_callback)
        best_effort_qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, depth=10)
        self.joint_pub = self.create_publisher(Int32, 'motor', best_effort_qos)
        self.create_subscription(Int32, 'joint_states', self.joint_callback, best_effort_qos)
        self.get_logger().info('Dummy node has been started.')

    def timer_callback(self):
        msg = Int32()
        if self.msg == 1:
            self.msg = 0
        else:
            self.msg = 1
        msg.data = self.msg
        self.joint_pub.publish(msg)

    def joint_callback(self, msg:Int32):
        self.get_logger().info(f'Received: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = DummyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
