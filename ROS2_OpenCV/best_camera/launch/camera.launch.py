import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # 🔹 best_camera config
    default_param = os.path.join(
        get_package_share_directory('best_camera'),
        'param',
        'picture.yaml'
    )

    param_dir = LaunchConfiguration('param_dir')

    # 🔹 apriltag config
    apriltag_config = os.path.join(
        get_package_share_directory('apriltag_ros'),
        'cfg',
        'tags_36h11.yaml'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'param_dir',
            default_value=default_param
        ),

        # ======================
        # 🔹 BEST CAMERA NODES
        # ======================
        Node(
            package='best_camera',
            executable='img_publisher',
            name='img_publisher',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='camera_pub',
            name='camera_pub',
            parameters=[param_dir],
            output='screen'),
    ])