import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from controller import JoystickController

# Define the vertices and edges of the block
vertices = [
    (1, -1, -1),  # 0
    (1, 1, -1),   # 1
    (-1, 1, -1),  # 2
    (-1, -1, -1), # 3
    (1, -1, 1),   # 4
    (1, 1, 1),    # 5
    (-1, -1, 1),  # 6
    (-1, 1, 1),   # 7
]

edges = [
    (0, 1), # Bottom front edge
    (1, 2), # Bottom right edge
    (2, 3), # Bottom back edge
    (3, 0), # Bottom left edge
    (4, 5), # Top front edge
    (5, 7), # Top right edge
    (7, 6), # Top back edge
    (6, 4), # Top left edge
    (0, 4), # Front left vertical edge
    (1, 5), # Front right vertical edge
    (2, 7), # Back right vertical edge
    (3, 6), # Back left vertical edge
]

def draw_block(position):
    """Draw the blue block at the specified position."""
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(0, 0, 1)  # Blue color
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()

def apply_deadzone(value, deadzone=0.2):
    """Apply deadzone handling to joystick axis values."""
    if abs(value) < deadzone:
        return 0
    return value

def main():
    pygame.init()
    
    # Get screen resolution and adjust for the taskbar
    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    
    # Create a window that fills the screen minus the taskbar
    display = (screen_width, screen_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)  # Move the camera back to view the cube
    
    controller = JoystickController()
    clock = pygame.time.Clock()
    
    block_position = [0, 0, 0]  # Initial position of the blue block

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        controller.update()
        
        # Read joystick input and apply deadzone
        left_stick_x = apply_deadzone(controller.joystick.get_axis(0))  # Left Stick X
        left_stick_y = apply_deadzone(controller.joystick.get_axis(1))  # Left Stick Y
        
        # Update block position based on joystick movement
        block_position[0] += left_stick_x * 0.1  # X-axis (left/right on the left stick)
        block_position[2] -= left_stick_y * 0.1  # Z-axis (forward/backward on the left stick)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_block(block_position)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
