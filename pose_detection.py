# pose_detection.py
# Handle all pose detection related functions

import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from math import hypot

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Setup the Pose functions with optimized parameters
pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=1)
pose_video = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)


def detect_pose(image, pose, draw=False, display=False):
    """
    Detect pose landmarks in the given image
    
    Args:
        image: Input image
        pose: Mediapipe pose object
        draw: Whether to draw landmarks on the image
        display: Whether to display the image
        
    Returns:
        Tuple of (processed image, pose detection results)
    """
    # Create a copy of the input image
    output_image = image.copy()
    
    # Convert the image from BGR into RGB format
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection
    results = pose.process(imageRGB)
    
    # Check if any landmarks are detected and are specified to be drawn
    if results.pose_landmarks and draw:
        # Draw Pose Landmarks on the output image
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                connections=mp_pose.POSE_CONNECTIONS,
                                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                            thickness=3, circle_radius=3),
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                            thickness=2, circle_radius=2))

    # Check if the original input image and the resultant image are specified to be displayed
    if display:
        # Display the original input image and the resultant image
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    else:
        # Return the output image and the results of pose landmarks detection
        return output_image, results


def check_hands_joined(image, results, draw=True, display=False):
    """
    Check if hands are joined based on wrist landmarks distance
    
    Args:
        image: Input image
        results: Pose detection results
        draw: Whether to draw hand status on the image
        display: Whether to display the image
        
    Returns:
        Tuple of (processed image, hands joined status)
    """
    # Create a copy of the input image
    output_image = image.copy()
    
    # Get the height and width of the input image
    height, width, _ = image.shape
    
    # Get the left wrist landmark x and y coordinates
    left_wrist_landmark = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width,
                          results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)

    # Get the right wrist landmark x and y coordinates
    right_wrist_landmark = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width,
                           results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)
    
    # Calculate the euclidean distance between the left and right wrist
    euclidean_distance = int(hypot(left_wrist_landmark[0] - right_wrist_landmark[0],
                                   left_wrist_landmark[1] - right_wrist_landmark[1]))
    
    # Compare the distance between the wrists with an appropriate threshold
    if euclidean_distance < 300:  # Threshold for detection
        hand_status = 'Hands Joined'
        color = (0, 255, 0)  # Green
    else:
        hand_status = 'Hands Not Joined'
        color = (0, 0, 255)  # Red
        
    # Check if the hand status and distance should be drawn on the image
    if draw:
        # Write the hand status on the image
        cv2.putText(output_image, hand_status, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        
        # Write the distance between wrists on the image
        cv2.putText(output_image, f'Distance: {euclidean_distance}', (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        
    if display:
        # Display the output image
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    else:
        # Return the output image and hand status
        return output_image, hand_status


def check_position_horizontal(image, results, draw=False, display=False):
    """
    Determine horizontal position (left, center, right) of the person based on 3-column grid
    
    Args:
        image: Input image
        results: Pose detection results
        draw: Whether to draw position on the image
        display: Whether to display the image
        
    Returns:
        Tuple of (processed image, horizontal position)
    """
    # Initialize horizontal position
    horizontal_position = None
    
    # Get the height and width of the image
    height, width, _ = image.shape
    
    # Create a copy of the input image
    output_image = image.copy()
    
    # Calculate the width of each column (divide screen into 3 columns)
    column_width = width // 3
    
    # Get the x-coordinate of the left and right shoulders
    left_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)
    right_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)
    
    # Calculate midpoint between shoulders to determine person's center position
    mid_x = (left_x + right_x) // 2
    
    # Determine horizontal position based on which column the person's midpoint is in
    if mid_x < column_width:
        horizontal_position = 'Left'
    elif mid_x < 2 * column_width:
        horizontal_position = 'Center'
    else:
        horizontal_position = 'Right'
        
    # Draw position information and grid if requested
    if draw:
        # Write the horizontal position on the image
        cv2.putText(output_image, horizontal_position, (5, height - 10), cv2.FONT_HERSHEY_PLAIN, 
                    2, (255, 255, 255), 3)
        
        # Draw column dividing lines (vertical)
        cv2.line(output_image, (column_width, 0), (column_width, height), (255, 255, 255), 2)
        cv2.line(output_image, (2 * column_width, 0), (2 * column_width, height), (255, 255, 255), 2)
        
        # Draw row dividing lines (horizontal) - 3 rows for symmetric 3x3 grid
        row_height = height // 3
        cv2.line(output_image, (0, row_height), (width, row_height), (255, 255, 255), 2)
        cv2.line(output_image, (0, 2 * row_height), (width, 2 * row_height), (255, 255, 255), 2)
        
        # Draw the midpoint of the person
        cv2.circle(output_image, (mid_x, height//2), 5, (0, 255, 0), -1)
        
    if display:
        # Display the output image
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    else:
        # Return the output image and horizontal position
        return output_image, horizontal_position


def check_position_vertical(image, results, MID_Y=None, draw=False, display=False):
    """
    Determine vertical position (top, middle, bottom) of the person based on 3-row grid
    
    Args:
        image: Input image
        results: Pose detection results
        MID_Y: Optional reference y-coordinate (not used in the grid-based approach)
        draw: Whether to draw posture on the image
        display: Whether to display the image
        
    Returns:
        Tuple of (processed image, posture)
    """
    # Get the height and width of the image
    height, width, _ = image.shape
    
    # Create a copy of the input image
    output_image = image.copy()
    
    # Calculate the height of each row (divide screen into 3 rows)
    row_height = height // 3
    
    # Get the y-coordinate of the left and right shoulders
    left_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)
    right_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)

    # Calculate the y-coordinate of the mid-point of both shoulders
    actual_mid_y = abs(right_y + left_y) // 2
    
    # Determine vertical position based on which row the person's midpoint is in
    if actual_mid_y < row_height:
        posture = 'Top' # Jumping
    elif actual_mid_y < 2 * row_height:
        posture = 'Middle' # Standing
    else:
        posture = 'Bottom' # Crouching
        
    # Draw position information and grid if requested
    if draw:
        # Write the vertical position on the image
        cv2.putText(output_image, posture, (5, height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        
        # Draw row dividing lines (already drawn in horizontal position function)
        
        # Draw the midpoint of the person
        cv2.circle(output_image, (width//2, actual_mid_y), 5, (0, 255, 0), -1)
        
    if display:
        # Display the output image
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    else:
        # Return the output image and posture
        return output_image, posture