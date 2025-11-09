#!/usr/bin/python3

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import launch
import os

leg_detector_path = get_package_share_directory('leg_detector')
forest_file_path = leg_detector_path + "/config/trained_leg_detector_res=0.33.yaml"

def generate_launch_description():
    return LaunchDescription([
        # Launching detect_leg_clusters node
        Node(
                package="leg_detector",
                executable="detect_leg_clusters",
                name="detect_leg_clusters",
                parameters= [
                    {"forest_file" : forest_file_path},
                    {"scan_topic" : "/scan"},
                    {"fixed_frame" : "laser"},
                    {"detection_threshold" : 0.2},
                ]
        ),
        # Launching joint_leg_tracker node
        Node(
            package="leg_detector",
            executable="joint_leg_tracker.py",
            name="joint_leg_tracker",
            parameters=[
                {"scan_topic" : "/scan"},
                {"fixed_frame" : "laser"},
                {"scan_frequency" : 10}
            ]    
        ),
        # Launching inflated_human_scan node
        Node(
            package="leg_detector",
            executable="inflated_human_scan",
            name="inflated_human_scan",
            parameters=[
                {"inflation_radius" : 1.0}
            ]
        ),
        # Launching local_occupancy_grid_mapping node
        Node(
            package="leg_detector",
            executable="local_occupancy_grid_mapping",
            name="local_occupancy_grid_mapping",
            parameters=[
                {"scan_topic" : "/scan"},
                {"fixed_frame" : "laser"},
            ]    
        )
    ])