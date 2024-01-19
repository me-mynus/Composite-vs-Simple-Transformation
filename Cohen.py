import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

# Region codes
INSIDE = 0b0000
LEFT = 0b0001
RIGHT = 0b0010
BOTTOM = 0b0100
TOP = 0b1000

# Clipping window coordinates
x_min, y_min, x_max, y_max = 100, 100, 500, 400

# Function to calculate region code for a point (x, y)
def compute_region_code(x, y):
    code = INSIDE

    if x < x_min:
        code |= LEFT
    elif x > x_max:
        code |= RIGHT

    if y < y_min:
        code |= BOTTOM
    elif y > y_max:
        code |= TOP

    return code

# Function to clip a line segment using Cohen-Sutherland algorithm
def cohen_sutherland(x1, y1, x2, y2):
    code1 = compute_region_code(x1, y1)
    code2 = compute_region_code(x2, y2)

    while (code1 | code2) != 0:  # Both endpoints are not inside the window
        if code1 & code2 != 0:  # Line segment is completely outside the window
            return None, None, None, None

        # Choose an endpoint outside the window
        if code1 != 0:
            code_out = code1
        else:
            code_out = code2

        # Find the intersection point
        if code_out & TOP:
            x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
            y = y_max
        elif code_out & BOTTOM:
            x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
            y = y_min
        elif code_out & RIGHT:
            y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
            x = x_max
        elif code_out & LEFT:
            y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
            x = x_min

        # Replace the outside endpoint with the intersection point
        if code_out == code1:
            x1, y1 = x, y
            code1 = compute_region_code(x1, y1)
        else:
            x2, y2 = x, y
            code2 = compute_region_code(x2, y2)

    return x1, y1, x2, y2

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 1)

    glBegin(GL_LINE_LOOP)
    glVertex2f(x_min, y_min)
    glVertex2f(x_max, y_min)
    glVertex2f(x_max, y_max)
    glVertex2f(x_min, y_max)
    glEnd()

    x1, y1, x2, y2 = 50, 50, 300, 300  # Initial line segment
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

    # Clip the line segment
    x1_c, y1_c, x2_c, y2_c = cohen_sutherland(x1, y1, x2, y2)

    if x1_c is not None:
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex2f(x1_c, y1_c)
        glVertex2f(x2_c, y2_c)
        glEnd()

    glFlush()

# Initialize OpenGL window
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    display()

glfw.init()

width = 550
height = 550

window = glfw.create_window(width, height, "Cohen", None, None)
glfw.make_context_current(window)
while not glfw.window_should_close(window):

    render()
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()
