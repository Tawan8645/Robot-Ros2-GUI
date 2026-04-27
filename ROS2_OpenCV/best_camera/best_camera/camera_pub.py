import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2

class threeCameraPublisher(Node):
    def __init__(self):
        super().__init__('three_camera_publisher')

        # กล้อง 2 ตัว
        self.cap1 = cv2.VideoCapture(1, cv2.CAP_V4L2)
        self.cap2 = cv2.VideoCapture(2, cv2.CAP_V4L2)
        self.cap3 = cv2.VideoCapture(3, cv2.CAP_V4L2)

        # publisher
        self.pub1 = self.create_publisher(CompressedImage, '/cam1/image/compressed', 4)
        self.pub2 = self.create_publisher(CompressedImage, '/cam2/image/compressed', 4)
        self.pub3 = self.create_publisher(CompressedImage, '/cam3/image/compressed', 4)

        # ตั้งค่า (ลดหน่วง)
        for cap in [self.cap1, self.cap2]:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
            cap.set(cv2.CAP_PROP_FPS, 300)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.timer = self.create_timer(0.0001, self.timer_callback)

    def timer_callback(self):
        # ===== CAM1 =====
        ret1, frame1 = self.cap1.read()
        if ret1:
            success1, enc1 = cv2.imencode('.jpg', frame1, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            if success1:
                msg1 = CompressedImage()
                msg1.format = "jpeg"
                msg1.data = enc1.tobytes()
                self.pub1.publish(msg1)

        # ===== CAM2 =====
        ret2, frame2 = self.cap2.read()
        if ret2:
            success2, enc2 = cv2.imencode('.jpg', frame2, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            if success2:
                msg2 = CompressedImage()
                msg2.format = "jpeg"
                msg2.data = enc2.tobytes()
                self.pub2.publish(msg2)
        
        # ===== CAM3 =====
        ret3, frame3 = self.cap3.read()
        if ret3:
            success3, enc3 = cv2.imencode('.jpg', frame3, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            if success3:
                msg3 = CompressedImage()
                msg3.format = "jpeg"
                msg3.data = enc3.tobytes()
                self.pub3.publish(msg3)

def main():
    rclpy.init()
    node = threeCameraPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.cap1.release()
    node.cap2.release()
    node.cap3.release()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()