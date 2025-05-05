# game_controller.py
# Handle all game control functions

import pyautogui
from time import sleep

class GameController:
    def __init__(self):
        # Game state variables
        self.game_started = False
        self.x_pos_index = 1  # 0: left, 1: center, 2: right
        self.y_pos_index = 1  # 0: crouch, 1: stand, 2: jump
        self.mid_y = None
        self.counter = 0
        self.num_of_frames = 10
        self.key_delay = 0  # delay between key presses in seconds
        self.activate_window_needed = True
    
    def is_game_started(self):
        """Return whether the game has started."""
        return self.game_started
    
    def move_left(self):
        """Press left arrow key and update position index."""
        # pyautogui.press('left')
        sleep(self.key_delay)
        self.x_pos_index -= 1
    
    def move_right(self):
        """Press right arrow key and update position index."""
        # pyautogui.press('right')
        sleep(self.key_delay)
        self.x_pos_index += 1
    
    def jump(self):
        """Press up arrow key and update position index."""
        pyautogui.press('up')
        print("Jump")
        sleep(self.key_delay)
        self.y_pos_index += 1
    
    def crouch(self):
        """Press down arrow key and update position index."""
        pyautogui.press('down')
        print("Crouch")
        sleep(self.key_delay)
        self.y_pos_index -= 1
    
    def stand(self):
        """Update position index to standing position."""
        self.y_pos_index = 1
    
    def press_space(self):
        """Press space key."""
        pyautogui.press('space')
        sleep(self.key_delay)
    
    def increment_counter(self):
        """Increment counter for hands joined detection."""
        self.counter += 1
        
    def reset_counter(self):
        """Reset counter for hands joined detection."""
        self.counter = 0
    
    def should_start_game(self):
        """Check if the counter has reached the threshold to start the game."""
        return self.counter == self.num_of_frames
    
    def start_game(self, left_y, right_y, frame_height):
        """
        Initialize game state variables when starting the game.
        
        Args:
            left_y: Y-coordinate of left shoulder
            right_y: Y-coordinate of right shoulder
            frame_height: Height of the video frame
        """
        self.game_started = True
        self.mid_y = abs(right_y + left_y) // 2
        
        # Directly activate the game window in the main thread
        if self.activate_window_needed:
            self._activate_game_window()
    
    def _activate_game_window(self):
        """Activate the game window and start the game."""
        try:
            # Get screen size
            screen_width, screen_height = pyautogui.size()
            
            # Click near the center of the screen where the game likely is
            pyautogui.click(x=screen_width//2, y=screen_height//2, button='left')
            sleep(0.5)
            
            # Press space to start (many games use this)
            pyautogui.press('space')
            
            self.activate_window_needed = False
        except Exception as e:
            # Log the error but continue execution
            print(f"Error activating game window: {e}")
    
    def process_horizontal_position(self, horizontal_position):
        """
        Process horizontal position and move character if needed.
        
        Args:
            horizontal_position: Current horizontal position ('Left', 'Center', 'Right')
        """
        # Map the desired position to index
        target_index = {'Left': 0, 'Center': 1, 'Right': 2}[horizontal_position]
        
        # Move left if needed
        while self.x_pos_index > target_index:
            self.move_left()
            
        # Move right if needed
        while self.x_pos_index < target_index:
            self.move_right()
    
    def process_vertical_position(self, posture):
        """
        Process vertical position and move character if needed.
        
        Args:
            posture: Current vertical posture ('Top', 'Middle', 'Bottom')
        """
        # Map the desired position to index
        target_index = {'Top': 2, 'Middle': 1, 'Bottom': 0}[posture]
        
        # Jump if top position detected and not already jumping
        if posture == 'Top' and self.y_pos_index != 2:
            pyautogui.press('up')
            print("Jump")
            sleep(self.key_delay)
            self.y_pos_index = 2
        # Crouch if bottom position detected and not already crouching
        elif posture == 'Bottom' and self.y_pos_index != 0:
            pyautogui.press('down')
            print("Crouch")
            sleep(self.key_delay)
            self.y_pos_index = 0
        # Stand if middle position detected and not already standing
        elif posture == 'Middle':
            self.y_pos_index = 1
            # No key press needed for middle position