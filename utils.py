# utils.py
# Utility functions for the application

import cv2
from time import time

class FPSCounter:
    """Class to calculate and display FPS"""
    def __init__(self):
        self.prev_time = time()
        self.fps = 0
    
    def update(self):
        """Update FPS calculation"""
        curr_time = time()
        time_diff = curr_time - self.prev_time
        
        # Update FPS if time difference is positive
        if time_diff > 0:
            self.fps = 1.0 / time_diff
            
        # Update previous time for next calculation
        self.prev_time = curr_time
        
        return self.fps
    
    def draw_fps(self, frame):
        """Draw FPS on the given frame"""
        cv2.putText(
            frame, 
            f'FPS: {int(self.fps)}', 
            (10, 30),
            cv2.FONT_HERSHEY_PLAIN, 
            2, 
            (0, 255, 0), 
            3
        )
        return frame


def setup_camera(camera_id=0, width=1280, height=960):
    """
    Setup camera with specified resolution
    
    Args:
        camera_id: Camera device ID (default: 0)
        width: Camera width resolution
        height: Camera height resolution
        
    Returns:
        OpenCV VideoCapture object
    """
    camera = cv2.VideoCapture(camera_id)
    camera.set(3, width)  # Width
    camera.set(4, height)  # Height
    
    return camera