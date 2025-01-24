import sys
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initial settings
cube_rotation_speed = 10  # Default RPM for the cube
cube_angle = 0.0  # Cube rotation angle

plane1_speed = 20  # RPM for the first plane (red)
plane2_speed = 40  # RPM for the second plane (white)

plane1_angle = 0.0  # Rotation angle for plane 1
plane2_angle = 0.0  # Rotation angle for plane 2

# Function to draw text at a specific location
def draw_text(text, x, y, z):
    glRasterPos3f(x, y, z)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Function to draw the 3D cube with markings
def draw_plane(color, angle, radius=0.8):
    glPushMatrix()
    
    glRotatef(angle, 0, 0, 1)  # Rotate around the Z-axis

    # Draw the plane (a circle with lines for angles)
    glBegin(GL_LINES)
    for angle in range(0, 360, 30):
        x = math.cos(math.radians(angle)) * radius
        y = math.sin(math.radians(angle)) * radius

        # Draw lines from center to the angle
        glVertex3f(0, 0, 0)  # Center of the plane
        glVertex3f(x, y, 0)  # Point on the circle
    glEnd()

    # Draw text for angles
    glColor3f(1, 1, 1)  # White text
    for angle in range(0, 360, 30):
        x = math.cos(math.radians(angle)) * radius
        y = math.sin(math.radians(angle)) * radius
        draw_text(f"{angle}°", x, y, 0.01)

    glPopMatrix()

# Function to update the rotation angles based on RPM
def update_rotation():
    global plane1_angle, plane2_angle

    time_per_rotation_plane1 = 60 / plane1_speed  # Time for one rotation for plane1 (seconds)
    angle_per_second_plane1 = 360 / time_per_rotation_plane1  # Degrees per second for plane1
    plane1_angle += angle_per_second_plane1 * (1 / 60.0)  # Assuming 60 FPS

    time_per_rotation_plane2 = 60 / plane2_speed  # Time for one rotation for plane2 (seconds)
    angle_per_second_plane2 = 360 / time_per_rotation_plane2  # Degrees per second for plane2
    plane2_angle += angle_per_second_plane2 * (1 / 60.0)  # Assuming 60 FPS

    if plane1_angle >= 360.0:
        plane1_angle -= 360.0
    if plane2_angle >= 360.0:
        plane2_angle -= 360.0

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up a perspective projection matrix
    gluPerspective(45, 800 / 600, 0.1, 50.0)  # 45-degree field of view, aspect ratio, near and far clipping planes
    
    # Position the camera a bit farther from the planes (z=3)
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)

    # Draw the red plane (rotation with RPM = 20)
    glColor3f(1, 0, 0)  # Red plane
    draw_plane(color=(1, 0, 0), angle=plane1_angle)

    # Draw the white plane (rotation with RPM = 40)
    glColor3f(1, 1, 1)  # White plane
    draw_plane(color=(1, 1, 1), angle=plane2_angle)

    glutSwapBuffers()

# Idle callback for continuous updates
def idle():
    update_rotation()
    glutPostRedisplay()

# Keyboard callback to adjust RPM
def keyboard(key, x, y):
    global plane1_speed, plane2_speed
    if key == b'+':
        plane1_speed = min(3000, plane1_speed + 10)  # Increase speed for plane1
        plane2_speed = min(3000, plane2_speed + 10)  # Increase speed for plane2
    elif key == b'-':
        plane1_speed = max(1, plane1_speed - 10)  # Decrease speed for plane1
        plane2_speed = max(1, plane2_speed - 10)  # Decrease speed for plane2
    elif key == b'q':
        sys.exit()

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Two Rotating Planes")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Enable transparency

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()

