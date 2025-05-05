# Body Pose Game Controller

A computer vision application that enables users to control games using body movements captured through a webcam. The system uses real-time pose detection to translate physical movements into game controls.

## Overview

This project uses the MediaPipe pose detection library to track a user's body position and converts those movements into keyboard inputs that can control games. The controller supports:

- Horizontal movement (left/center/right) by tracking the user's shoulders
- Vertical movement (crouch/stand/jump) based on body position
- Game start/pause by joining hands together

## Features

- **Real-time pose detection** using MediaPipe
- **Intuitive gesture controls**:
  - Join hands to start/resume the game
  - Move left or right to control horizontal movement
  - Jump up or crouch down to control vertical movement
- **Visual feedback** with pose landmarks and grid overlay
- **FPS counter** to monitor performance
- **Configurable settings** for camera resolution and control sensitivity

## Requirements

- Python 3.10+
- Webcam
- The following Python packages:
  - opencv-python
  - mediapipe
  - pyautogui
  - matplotlib

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/body-pose-game-controller.git
cd body-pose-game-controller
```

2. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Run the main application:
```
python main.py
```

2. Position yourself in front of the webcam.
3. Join both hands together to start the game.
4. Control your game character using body movements:
   - Lean left or right to move horizontally
   - Stand up straight to maintain normal position
   - Jump up to make your character jump
   - Crouch down to make your character duck or slide

5. Press ESC to exit the application.

## Project Structure

- `main.py` - Main application entry point that processes camera frames
- `pose_detection.py` - Contains functions for detecting and analyzing body poses
- `game_controller.py` - Handles game control logic and key press simulation
- `utils.py` - Utility functions for FPS calculation and camera setup
- `requirements.txt` - List of required Python packages

## How It Works

1. The webcam captures video frames
2. MediaPipe detects body pose landmarks in each frame
3. The application analyzes the position of key landmarks:
   - Wrists for hand joining detection
   - Shoulders for horizontal movement
   - Upper body position for vertical movement
4. PyAutoGUI simulates keyboard presses based on detected movements
5. Visual feedback is provided on screen with landmarks and position information

## Customization

You can modify the following parameters in the code:

- Camera resolution in `utils.py`
- Frame rate limit in `main.py`
- Detection thresholds in `pose_detection.py`
- Key mappings in `game_controller.py`

## Limitations

- Best performance in well-lit environments
- Limited to games that use keyboard controls
- Requires clear view of the user's body
- May have latency depending on your hardware

## Future Improvements

- Support for more complex gestures
- Customizable control mapping through a UI
- Support for game controller emulation
- Performance optimizations for lower-end hardware
- Auto-calibration based on user's body proportions

## License

[Specify your license here]

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for the pose detection framework
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for keyboard control simulation

## Author

Thanabordee Nammungkhun

---

Feel free to contribute to this project by submitting pull requests or opening issues for bugs and feature requests.