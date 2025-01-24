from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtOpenGL import QOpenGLWindow
from OpenGL.GL import *

class MyOpenGLWindow(QOpenGLWindow):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        """This method is called when OpenGL context is initialized."""
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set the background color to black

    def paintGL(self):
        """This method is called to render the OpenGL scene."""
        glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen
        # You can add your OpenGL rendering code here, for example:
        glColor3f(1.0, 0.0, 0.0)  # Set color to red
        glBegin(GL_TRIANGLES)  # Start drawing a triangle
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.0, 0.5)
        glEnd()  # Finish drawing the triangle
        self.update()

if __name__ == "__main__":
    app = QApplication([])  # Create the Qt application
    window = MyOpenGLWindow()  # Create the OpenGL window
    window.resize(800, 600)  # Set the window size
    window.show()  # Show the window
    app.exec()  # Run the application loop

