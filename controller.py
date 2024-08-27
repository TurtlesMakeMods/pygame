import pygame

# Button and Axis Mappings for Xbox 360 Controller
button_names = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "LB",
    5: "RB",
    6: "Back",
    7: "Start",
    8: "Left Stick Press",
    9: "Right Stick Press",
    10: "Xbox"
}

axis_names = {
    0: "Left Stick X",
    1: "Left Stick Y",
    2: "Right Stick X",
    3: "Right Stick Y",
    4: "Left Trigger",
    5: "Right Trigger"
}

# Deadzone threshold (ignore small joystick movements)
DEADZONE = 0.2

def apply_deadzone(value, deadzone=DEADZONE):
    """Apply deadzone handling to joystick axis values."""
    if abs(value) < deadzone:
        return 0
    return value

class JoystickController:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.axis_x = 0
        self.axis_y = 0

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            print("No joystick detected")

    def update(self):
        if self.joystick:
            pygame.event.pump()  # Process event queue
            self.axis_x = apply_deadzone(self.joystick.get_axis(0))  # Left Stick X
            self.axis_y = apply_deadzone(self.joystick.get_axis(1))  # Left Stick Y

    def get_movement(self):
        return self.axis_x * 0.1, self.axis_y * 0.1  # Scale factor for movement
