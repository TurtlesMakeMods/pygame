import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from controller_data_sim import JoystickController

# Define the vertices and edges of the cube
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

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    clock = pygame.time.Clock()
    controller = JoystickController()
    
    angle_x, angle_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        controller.update()
        rot_x, rot_y = controller.get_rotation()
        
        # Apply joystick inputs to cube rotation
        angle_x += rot_y  # Use joystick's Y axis for X rotation
        angle_y += rot_x  # Use joystick's X axis for Y rotation
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(angle_x, 1, 0, 0)  # Rotate around X-axis
        glRotatef(angle_y, 0, 1, 0)  # Rotate around Y-axis
        draw_cube()
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()