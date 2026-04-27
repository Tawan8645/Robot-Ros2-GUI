import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage
from apriltag_msgs.msg import AprilTagDetectionArray
from cv_bridge import CvBridge
import cv2

class TagOverlay(Node):
    def __init__(self):
        super().__init__('tag_overlay')

        self.bridge = CvBridge()

        # Subscribe
        self.image_sub = self.create_subscription(
            Image, '/image_raw', self.image_callback, 4)

        self.det_sub = self.create_subscription(
            AprilTagDetectionArray, '/detections', self.det_callback, 4)

        # 🔹 Publish (ของเดิม)
        self.image_pub = self.create_publisher(Image, '/image_tag', 4)

        # 🔥 เพิ่มสำหรับเว็บ
        self.image_pub_compressed = self.create_publisher(
            CompressedImage, '/detect_marker/image_raw/compressed', 1)

        self.detections = []

    def det_callback(self, msg):
        self.detections = msg.detections

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # วาด ID ลงภาพ
        for det in self.detections:
            tag_id = det.id
            x = int(det.centre.x)
            y = int(det.centre.y)

            cv2.putText(frame, f"ID:{tag_id}", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (98,0,255), 2)

        # 🔹 publish แบบ ROS ปกติ
        out_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        out_msg.header = msg.header
        self.image_pub.publish(out_msg)

        # 🔥 publish สำหรับเว็บ (compressed)
        success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if success:
            msg_comp = CompressedImage()
            msg_comp.header = msg.header
            msg_comp.format = "jpeg"
            msg_comp.data = buffer.tobytes()

            self.image_pub_compressed.publish(msg_comp)


def main():
    rclpy.init()
    node = TagOverlay()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()