"""
A simple program to read USB Xbox 360 controller inputs using pygame
Author: TurtlesMakeMods (Titus Domey)
"""

import pygame
import time

# Initialize pygame
pygame.init()

# Initialize the joystick (controller)
pygame.joystick.init()

# Check if the controller is connected
if pygame.joystick.get_count() == 0:
    print("No controller connected")
    exit()

# Getting the controller
controller = pygame.joystick.Joystick(0)
controller.init()

print(f"Controller name: {controller.get_name()}")

# Loop that continues to check for controller inputs
try:
    while True:
        for event in pygame.event.get():
            # Checks for button press events
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")

            # Checks for button release events
            if event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")

            # Checks for joystick (analog stick) movement events
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value
                print(f"Axis {axis} moved to {value}")

            # Checks for D-pad (hat) movement events
            if event.type == pygame.JOYHATMOTION:
                hat = event.hat
                value = event.value
                print(f"Hat {hat} moved to {value}")

        # Sleeping to avoid high CPU usage
        time.sleep(0.01)

# Exit the loop if interrupted
except KeyboardInterrupt:
    print("exiting...")

# Cleaning up resources
finally:
    pygame.joystick.quit()
    pygame.quit()