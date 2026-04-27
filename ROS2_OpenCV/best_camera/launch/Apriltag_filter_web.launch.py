import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


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
        # 🔥 run React web
        ExecuteProcess(
            cmd=['yarn', 'start'],
            cwd='/home/tawan-master/iRAP-Minirescue-GUI',  # 👈 แก้ตรงนี้
            output='screen'
        ),

        # ======================
        # 🔹 BEST CAMERA NODES
        # ======================
        Node(
            package='best_camera',
            executable='edge',
            name='edge',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='img_control',
            name='img_control',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='optical_flow',
            name='optical_flow',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='cartoon',
            name='cartoon',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='gray',
            name='gray',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='aruco',
            name='aruco',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='best_camera',
            executable='showid',
            name='showid',
            parameters=[param_dir],
            output='screen'),

        # ======================
        # 🔥 APRILTAG NODE
        # ======================
        Node(
            package='apriltag_ros',
            executable='apriltag_node',
            name='apriltag',
            parameters=[apriltag_config],
            remappings=[
                ('image_rect', '/image_raw'),
                ('camera_info', '/camera_info')
            ],
            output='screen'),
        # ======================
        # 🖥 IMAGE VIEW (GUI)
        # ======================
        Node(
            package='rqt_image_view',
            executable='rqt_image_view',
            name='image_view',
            output='screen'),

        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
            name='rosbridge',
            output='screen'),

    ])