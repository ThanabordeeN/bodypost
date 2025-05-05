# main.py
# Main application for body pose game controller
# Required packages:
# pip install opencv-python
# pip install pyautogui
# pip install mediapipe
# pip install matplotlib

import cv2
from time import time, sleep

# Import modules from our project
from pose_detection import (
    mp_pose, pose_video, detect_pose, 
    check_hands_joined, check_position_horizontal, check_position_vertical
)
from game_controller import GameController
from utils import FPSCounter, setup_camera


def process_frame(frame, controller, fps_counter):
    """Process a single video frame"""
    # Flip the frame horizontally for natural visualization
    frame = cv2.flip(frame, 1)
    
    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape
    
    # Perform pose detection
    frame, results = detect_pose(frame, pose_video, draw=controller.is_game_started())
    
    # Check if pose landmarks are detected
    if results.pose_landmarks:
        if controller.is_game_started():
            # Process horizontal movement
            frame, horizontal_position = check_position_horizontal(frame, results, draw=True)
            controller.process_horizontal_position(horizontal_position)
            
            # Process vertical movement if mid_y is set
            if controller.mid_y:
                frame, posture = check_position_vertical(frame, results, controller.mid_y, draw=True)
                controller.process_vertical_position(posture)
        else:
            # Show instructions to start the game
            cv2.putText(
                frame, 
                'JOIN BOTH HANDS TO START THE GAME.', 
                (5, frame_height - 10), 
                cv2.FONT_HERSHEY_PLAIN,
                2, 
                (0, 255, 0), 
                3
            )
        
        # Check if hands are joined
        _, hand_status = check_hands_joined(frame, results)
        
        if hand_status == 'Hands Joined':
            controller.increment_counter()
            
            # Start or resume game if counter threshold is reached
            if controller.should_start_game():
                if not controller.is_game_started():
                    # Get shoulder coordinates to calculate mid_y
                    left_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame_height)
                    right_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame_height)
                    
                    # Start the game
                    controller.start_game(left_y, right_y, frame_height)
                # else:
                    # Resume game after character death
                    # controller.press_space()
                
                # controller.reset_counter()
        else:
            controller.reset_counter()
    else:
        controller.reset_counter()
    
    # Update FPS counter and draw on frame
    fps_counter.update()
    frame = fps_counter.draw_fps(frame)
    
    return frame


def main():
    """Main function to run the game controller"""
    # Setup camera
    camera_video = setup_camera()
    
    # Create named window for resizing
    cv2.namedWindow('Body Pose Game Controller', cv2.WINDOW_NORMAL)
    
    # Initialize game controller and FPS counter
    controller = GameController()
    fps_counter = FPSCounter()
    
    # Limit update rate to prevent too many PyAutoGUI commands at once
    frame_limit = 60  # max frames per second to process
    frame_delay = 1.0 / frame_limit
    last_frame_time = 0
    
    # Main loop
    try:
        while camera_video.isOpened():
            # Check for key press to exit
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
                
            # Rate limiting to prevent processing too many frames
            current_time = time()
            if current_time - last_frame_time < frame_delay:
                # Skip this frame if we're processing too quickly
                sleep(0.001)  # Small sleep to prevent CPU hogging
                continue
                
            last_frame_time = current_time
            
            # Read a frame
            ok, frame = camera_video.read()
            
            if not ok:
                continue
            
            # Process the frame directly in the main thread
            processed_frame = process_frame(frame, controller, fps_counter)
            cv2.imshow('Body Pose Game Controller', processed_frame)
    
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Release resources
        camera_video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()