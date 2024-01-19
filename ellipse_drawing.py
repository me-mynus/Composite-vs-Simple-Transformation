import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import math


width, height = 800, 600
rx, ry = 200, 150  # Semi-major and semi-minor axes lengths
xc, yc = width // 2, height // 2  # Ellipse center

# Midpoint Ellipse Drawing Algorithm
def draw_ellipse(rx, ry, xc, yc):
    x, y = 0, ry

    p1 = ry**2 - rx**2 * ry + 0.25 * rx**2      #For Region 1
    plot_points(xc, yc, x, y)

    while 2 * (ry**2) * x < 2 * (rx**2) * y:
        x += 1
        if p1 < 0:
            p1 = p1 + 2 * (ry**2) * x + (ry**2)
        else:
            y -= 1
            p1 = p1 + 2 * (ry**2) * x - 2 * (rx**2) * y + (ry**2)

        plot_points(xc, yc, x, y)

    p2 = (ry**2) * (x + 0.5)**2 + (rx**2) * (y - 1)**2 - (rx**2) * (ry**2)      #For Region 2
    while y >= 0:
        y -= 1
        if p2 > 0:
            p2 = p2 - 2 * (rx**2) * y + (rx**2)
        else:
            x += 1
            p2 = p2 + 2 * (ry**2) * x - 2 * (rx**2) * y + (rx**2)

        plot_points(xc, yc, x, y)

# Function to plot points in all octants
def plot_points(xc, yc, x, y):
    glBegin(GL_POINTS)
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 1)

    draw_ellipse(rx, ry, xc, yc)

    glFlush()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    display()

glfw.init()

width = 800
height = 550

window = glfw.create_window(width, height, "Ellipse Drawing", None, None)
glfw.make_context_current(window)
while not glfw.window_should_close(window):

    render()
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()
