import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QOpenGLContext
from PyQt6.QtOpenGL import QOpenGLWindow
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import glutInit, glutInitDisplayMode, GLUT_DOUBLE, GLUT_RGB


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


# Function to draw the 3D plane with markings
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


# OpenGL Window for rendering the rotating planes
class OpenGLWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout to hold the OpenGL window
        layout = QVBoxLayout(self)
        
        # Create and initialize the OpenGL window
        self.opengl_window = OpenGLWindow()
        
        # Create a container widget for the OpenGL window
        self.opengl_container = QWidget.createWindowContainer(self.opengl_window, self)

        layout.addWidget(self.opengl_container)

        self.setLayout(layout)


class OpenGLWindow(QOpenGLWindow):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        # Initialize GLUT here before using any GLUT functionality
        glutInit(sys.argv)  # Initialize GLUT
        glClearColor(0, 0, 0, 1)  # Set background color to black
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Enable transparency

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)  # Set up the perspective projection
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Call the function to update the rotation angles based on the RPM
        update_rotation()

        # Position the camera a bit farther from the planes (z=3)
        gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)

        # Draw the red plane (rotation with RPM = 20)
        glColor3f(1, 0, 0)  # Red plane
        draw_plane(color=(1, 0, 0), angle=plane1_angle)

        # Draw the white plane (rotation with RPM = 40)
        glColor3f(1, 1, 1)  # White plane
        draw_plane(color=(1, 1, 1), angle=plane2_angle)

        self.update()


# PyQt6 GUI with RPM control sliders
class RPMControlWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('RPM Control')
        self.setGeometry(100, 100, 400, 200)

        # Layout and controls
        layout = QVBoxLayout()

        self.plane1_label = QLabel('Plane 1 RPM: 20', self)
        self.plane1_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.plane1_slider.setRange(1, 10000)
        self.plane1_slider.setValue(plane1_speed)
        self.plane1_slider.valueChanged.connect(self.update_plane1_rpm)

        self.plane2_label = QLabel('Plane 2 RPM: 40', self)
        self.plane2_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.plane2_slider.setRange(1, 10000)
        self.plane2_slider.setValue(plane2_speed)
        self.plane2_slider.valueChanged.connect(self.update_plane2_rpm)

        layout.addWidget(self.plane1_label)
        layout.addWidget(self.plane1_slider)
        layout.addWidget(self.plane2_label)
        layout.addWidget(self.plane2_slider)

        self.setLayout(layout)

    def update_plane1_rpm(self, value):
        global plane1_speed
        plane1_speed = value
        self.plane1_label.setText(f'Plane 1 RPM: {value}')

    def update_plane2_rpm(self, value):
        global plane2_speed
        plane2_speed = value
        self.plane2_label.setText(f'Plane 2 RPM: {value}')


# Main function
def main():
    app = QApplication(sys.argv)

    # Create the RPM control window
    rpm_window = RPMControlWindow()
    rpm_window.show()

    # Create the OpenGL widget (which now includes the OpenGL window)
    opengl_widget = OpenGLWidget()
    opengl_widget.setGeometry(100, 100, 800, 600)
    opengl_widget.show()

    # Create a splitter
    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.addWidget(opengl_widget)
    splitter.addWidget(rpm_window)

    # Set the layout to use the splitter
    main_layout = QVBoxLayout()
    main_layout.addWidget(splitter)

    # Create a QWidget to hold the layout
    main_widget = QWidget()
    main_widget.setLayout(main_layout)
    main_widget.show()

    app.exec()


if __name__ == "__main__":
    main()

