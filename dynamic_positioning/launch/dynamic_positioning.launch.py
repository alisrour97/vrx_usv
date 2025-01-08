from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dynamic_positioning',
            executable='dynamic_positioning_node',
            name='dynamic_positioning_node',
            output='screen',
        ),
    ])
