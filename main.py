import sys
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initial settings
cube_rotation_speed = 60  # Default RPM
cube_angle = 0.0  # Cube rotation angle

# Function to draw text at a specific location
def draw_text(text, x, y, z):
    glRasterPos3f(x, y, z)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Function to draw the 3D cube with markings
def draw_cube():
    glBegin(GL_QUADS)

    # Front face (z = 1.0)
    glColor3f(1, 0, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Back face (z = -1.0)
    glColor3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, -1, -1)

    # Top face (y = 1.0)
    glColor3f(0, 0, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)

    # Bottom face (y = -1.0)
    glColor3f(1, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)

    # Right face (x = 1.0)
    glColor3f(1, 0, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)

    # Left face (x = -1.0)
    glColor3f(0, 1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)

    glEnd()

    # Add markings on the front face
    glColor3f(1, 1, 1)  # White text
    for angle in range(0, 360, 30):
        x = math.cos(math.radians(angle)) * 0.8
        y = math.sin(math.radians(angle)) * 0.8
        draw_text(f"{angle}°", x, y, 1.01)

# Function to update the rotation angle based on RPM
def update_cube_rotation():
    global cube_angle
    global cube_rotation_speed

    time_per_rotation = 60 / cube_rotation_speed  # Time for one rotation (seconds)
    angle_per_second = 360 / time_per_rotation  # Degrees per second
    cube_angle += angle_per_second * (1 / 60.0)  # Assuming 60 FPS

    if cube_angle >= 360.0:
        cube_angle -= 360.0

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Position the camera at the center of the cube
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)

    # Apply rotation to the cube
    glRotatef(cube_angle, 0, 1, 0)
    draw_cube()

    glutSwapBuffers()

# Idle callback for continuous updates
def idle():
    update_cube_rotation()
    glutPostRedisplay()

# Keyboard callback to adjust RPM
def keyboard(key, x, y):
    global cube_rotation_speed
    if key == b'+':
        cube_rotation_speed = min(3000, cube_rotation_speed + 100)  # Increase speed
    elif key == b'-':
        cube_rotation_speed = max(1, cube_rotation_speed - 100)  # Decrease speed
    elif key == b'q':
        sys.exit()

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Cube with Rotation")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()

