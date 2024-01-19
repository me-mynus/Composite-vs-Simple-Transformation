import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

rectangle = [
    [-0.5, -0.2, 1],
    [0.5, -0.2, 1],
    [0.5, 0.5, 1],
    [-0.5, 0.5, 1]
]
translation_vector = [0.1, 0.2]
rotation_angle = 45.0
scaling_factors = [1.5, 1.5]
reflection_axis = "x"
shearing_factors = [0.2, 0.2]

# Function to draw a rectangle
def draw_rectangle(rectangle):
    glBegin(GL_QUADS)
    for vertex in rectangle:
        glVertex2f(vertex[0], vertex[1])
    glEnd()

# Function to apply 2D translation
def translate():
    glTranslatef(translation_vector[0], translation_vector[1], 0.0)
    draw_rectangle(rectangle)

# Function to apply 2D rotation
def rotate():
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    draw_rectangle(rectangle)

# Function to apply 2D scaling
def scale():
    glScalef(scaling_factors[0], scaling_factors[1], 1.0)
    draw_rectangle(rectangle)

# Function to apply 2D reflection
def reflect():
    global rectangle
    if reflection_axis == 'x':
        reflection_matrix = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1],
        ])
    elif reflection_axis == 'y':
        reflection_matrix = np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        ])
    else:
        raise ValueError("Invalid reflection axis")
    rectangle2 = np.dot(rectangle, reflection_matrix.T)
    draw_rectangle(rectangle2)


# Function to apply 2D shearing
def shear():
    global rectangle
    shearing_matrix = np.array([
        [1, shearing_factors[0], 0],
        [shearing_factors[1], 1, 0],
        [0, 0, 1]
])
    rectangle2 = np.dot(rectangle, shearing_matrix.T)
    draw_rectangle(rectangle2)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    glColor3f(1, 1, 1)
    draw_rectangle(rectangle)
    
    glColor3f(0,1,0)
    #translate()
    #rotate()
    #scale()
    #reflect()
    #shear()
    
    glFlush()


# Keyboard callback function
def key_callback(window, key, scancode, action, mods):
    global translation_vector, rotation_angle, scaling_factors, reflection_axes, shearing_factors

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_W:
            translation_vector[1] += 0.1
        elif key == glfw.KEY_S:
            translation_vector[1] -= 0.1
        elif key == glfw.KEY_A:
            translation_vector[0] -= 0.1
        elif key == glfw.KEY_D:
            translation_vector[0] += 0.1
        elif key == glfw.KEY_UP:
            scaling_factors[1] += 0.1
        elif key == glfw.KEY_DOWN:
            scaling_factors[1] -= 0.1
        elif key == glfw.KEY_LEFT:
            scaling_factors[0] -= 0.1
        elif key == glfw.KEY_RIGHT:
            scaling_factors[0] += 0.1
        elif key == glfw.KEY_R:
            rotation_angle += 10.0
        elif key == glfw.KEY_F:
            reflection_axes[0] *= -1.0
        elif key == glfw.KEY_H:
            shearing_factors[0] += 0.1
        elif key == glfw.KEY_V:
            shearing_factors[1] += 0.1

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
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()
