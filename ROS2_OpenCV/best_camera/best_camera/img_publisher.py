import rclpy 
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge 
import cv2

class ImgPublisher(Node):
    def __init__(self):
        super().__init__('img_publisher')

        # 🔹 ของเดิม (ไม่ลบ)
        self.publisher = self.create_publisher(Image, '/camera', 4)

        # 🔹 เพิ่มใหม่สำหรับ AprilTag
        self.image_pub = self.create_publisher(Image, '/image_raw', 4)
        self.info_pub = self.create_publisher(CameraInfo, '/camera_info', 4)

        # Parameter
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)

        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value

        # Timer (30 FPS)
        self.timer = self.create_timer(1/100, self.timer_callback)

        # OpenCV Camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not self.cap.isOpened():
            self.get_logger().error("Cannot open camera")
        
        self.bridge = CvBridge()

        # 🔹 เพิ่ม camera_info (fake สำหรับ test ID)
        self.cam_info = CameraInfo()
        self.cam_info.width = self.width
        self.cam_info.height = self.height
        self.cam_info.k = [1.0, 0.0, self.width/2,
                           0.0, 1.0, self.height/2,
                           0.0, 0.0, 1.0]

        self.get_logger().info(f"Camera started: {self.width}x{self.height}")

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warning("Failed to read frame")
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()

        # 🔹 publish ของเดิม
        self.publisher.publish(msg)

        # 🔹 publish เพิ่ม
        self.image_pub.publish(msg)

        self.cam_info.header = msg.header
        self.info_pub.publish(self.cam_info)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main():
    rclpy.init()
    node = ImgPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()