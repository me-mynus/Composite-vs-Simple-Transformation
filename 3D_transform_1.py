import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables
width, height = 800, 600
translate_x, translate_y, translate_z = 0.0, 0.0, 0.0
rotate_x, rotate_y, rotate_z = 0.0, 0.0, 0.0
scale_factor = 1.5

# Function to draw a 3D cube
def draw_cube():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glBegin(GL_QUADS)
    
    glColor3f(0, 1, 0)
    glVertex3f(0.3, 0.3, -0.3)
    glVertex3f(-0.3, 0.3, -0.3)
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f(0.3, 0.3, 0.3)
    
    glColor3f(1, 0, 0)
    glVertex3f(0.3, -0.3, 0.3)
    glVertex3f(-0.3, -0.3, 0.3)
    glVertex3f(-0.3, -0.3, -0.3)
    glVertex3f(0.3, -0.3, -0.3)

    glColor3f(0, 0, 1)
    glVertex3f(0.3, 0.3, 0.3)
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f(-0.3, -0.3, 0.3)
    glVertex3f(0.3, -0.3, 0.3)

 
    glColor3f(1, 1, 0)
    glVertex3f(0.3, -0.3, -0.3)
    glVertex3f(-0.3, -0.3, -0.3)
    glVertex3f(-0.3, 0.3, -0.3)
    glVertex3f(0.3, 0.3, -0.3)


    glColor3f(0.0, 1, 1)
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f(-0.3, 0.3, -0.3)
    glVertex3f(-0.3, -0.3, -0.3)
    glVertex3f(-0.3, -0.3, 0.3)

    glColor3f(1, 0, 1)
    glVertex3f(0.3, 0.3, -0.3)
    glVertex3f(0.3, 0.3, 0.3)
    glVertex3f(0.3, -0.3, 0.3)
    glVertex3f(0.3, -0.3, -0.3)
    glEnd()
    
# Function to apply 3D translation
def translate():
    glTranslatef(translate_x, translate_y, translate_z)

# Function to apply 3D rotation
def rotate():
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)
    glRotatef(rotate_z, 0, 0, 1)

# Function to apply 3D scaling
def scale():
    glScalef(scale_factor, scale_factor, scale_factor)

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    translate()
    rotate()
    scale()
    
    draw_cube()
    glFlush()

# Reshape function
def reshape(window, w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width/height), 0.3, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Keyboard callback function
def key_callback(window, key, scancode, action, mods):
    global translate_x, translate_y, translate_z, rotate_x, rotate_y, rotate_z, scale_factor

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_W:
            translate_z += 0.3
        elif key == glfw.KEY_S:
            translate_z -= 0.3
        elif key == glfw.KEY_A:
            translate_x -= 0.3
        elif key == glfw.KEY_D:
            translate_x += 0.3
        elif key == glfw.KEY_UP:
            rotate_x += 5
        elif key == glfw.KEY_DOWN:
            rotate_x -= 5
        elif key == glfw.KEY_LEFT:
            rotate_y -= 5
        elif key == glfw.KEY_RIGHT:
            rotate_y += 5
        elif key == glfw.KEY_EQUAL:
            scale_factor += 0.3
        elif key == glfw.KEY_MINUS:
            scale_factor -= 0.3

# Initialize OpenGL window
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    display()

glfw.init()

width = 800
height = 550

window = glfw.create_window(width, height, "2D Transform", None, None)
glfw.make_context_current(window)

while not glfw.window_should_close(window):
    render()
    glfw.set_key_callback(window, key_callback)
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()
