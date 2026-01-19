"""
Utility functions for the Fall Detection System
"""

import cv2
import numpy as np
from datetime import datetime


def draw_keypoints(frame, keypoints, radius=5, color=(0, 255, 255)):
    """
    Draw pose keypoints on frame.
    
    Args:
        frame: Input frame
        keypoints: Array of keypoints with [x, y, confidence]
        radius: Radius of keypoint circles
        color: BGR color tuple
    """
    for kpt in keypoints:
        if len(kpt) >= 3 and kpt[2] > 0.3:  # Confidence threshold
            x, y = int(kpt[0]), int(kpt[1])
            cv2.circle(frame, (x, y), radius, color, -1)


def draw_skeleton(frame, keypoints, connections, color=(0, 255, 0), thickness=2):
    """
    Draw skeleton by connecting keypoints.
    
    Args:
        frame: Input frame
        keypoints: Array of keypoints
        connections: List of tuples connecting keypoint indices
        color: BGR color tuple
        thickness: Line thickness
    """
    for start_idx, end_idx in connections:
        if (start_idx < len(keypoints) and end_idx < len(keypoints)):
            start = keypoints[start_idx]
            end = keypoints[end_idx]
            
            if start[2] > 0.3 and end[2] > 0.3:  # Both points have confidence
                pt1 = (int(start[0]), int(start[1]))
                pt2 = (int(end[0]), int(end[1]))
                cv2.line(frame, pt1, pt2, color, thickness)


def get_coco_connections():
    """
    Get COCO format skeleton connections for drawing.
    Returns list of keypoint pairs to connect.
    """
    return [
        # Head
        (0, 1), (0, 2), (1, 3), (2, 4),
        # Body
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
        (5, 11), (6, 12), (11, 12),
        # Legs
        (11, 13), (13, 15), (12, 14), (14, 16)
    ]


def log_event(event_type, details=""):
    """
    Log events with timestamp.
    
    Args:
        event_type: Type of event (FALL, PERSON_DETECTED, etc.)
        details: Additional details
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_message = f"[{timestamp}] {event_type}"
    if details:
        log_message += f" - {details}"
    print(log_message)


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_angle(point1, point2, point3):
    """
    Calculate angle between three points.
    Returns angle in degrees.
    """
    v1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
    v2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
    angle = np.arccos(np.clip(cos_angle, -1, 1))
    
    return np.degrees(angle)


def is_point_in_region(point, region_box):
    """
    Check if point is inside a rectangular region.
    
    Args:
        point: (x, y) coordinate
        region_box: (x1, y1, x2, y2) bounding box
    
    Returns:
        bool: True if point is inside region
    """
    x, y = point
    x1, y1, x2, y2 = region_box
    return x1 <= x <= x2 and y1 <= y <= y2


def smooth_trajectory(trajectory, window_size=5):
    """
    Smooth trajectory using moving average.
    
    Args:
        trajectory: List of (x, y) coordinates
        window_size: Size of smoothing window
    
    Returns:
        Smoothed trajectory
    """
    if len(trajectory) < window_size:
        return trajectory
    
    smoothed = []
    for i in range(len(trajectory)):
        start = max(0, i - window_size // 2)
        end = min(len(trajectory), i + window_size // 2 + 1)
        window = trajectory[start:end]
        avg_x = np.mean([p[0] for p in window])
        avg_y = np.mean([p[1] for p in window])
        smoothed.append((avg_x, avg_y))
    
    return smoothed
