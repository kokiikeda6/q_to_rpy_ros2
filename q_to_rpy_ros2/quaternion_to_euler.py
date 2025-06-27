import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from rclpy.qos import QoSProfile
from scipy.spatial.transform import Rotation as R
import numpy as np

class QuaternionToEulerNode(Node):
    def __init__(self):
        super().__init__('quaternion_to_euler')

        self.flag = False
        self.init_rotation = None  # 初期回転用のRotationオブジェクト

        self.create_subscription(
            Pose,
            "/end_pose",
            self.callback_quaternion_to_euler,
            qos_profile=QoSProfile(depth=10)
        )
        self.get_logger().info("quaternion_to_euler node started.")

    def callback_quaternion_to_euler(self, msg):
        # クォータニオンを取得
        quat = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        current_rot = R.from_quat(quat)

        if not self.flag:
            self.init_rotation = current_rot
            self.flag = True
            self.get_logger().info("Initial orientation set.")
            return

        # 初期姿勢との差分回転
        delta_rot = self.init_rotation.inv() * current_rot

        # RPY角（xyz = Roll, Pitch, Yaw）
        delta_rpy = delta_rot.as_euler('xyz', degrees=True)

        self.get_logger().info(
            f"ΔRoll: {delta_rpy[2]:.2f}°, ΔPitch: {delta_rpy[1]:.2f}°, ΔYaw: {delta_rpy[0]:.2f}°"
        )

def main():
    rclpy.init()
    node = QuaternionToEulerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
