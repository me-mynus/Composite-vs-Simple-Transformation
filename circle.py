import glfw
from OpenGL.GL import *

def draw_circle(radius, xc, yc):
    x = 0
    y = radius
    p = 5/4 - radius
    
    while (x <= y):
        draw_symmetric(x, y, xc, yc)
        x += 1
        if (p <= 0):
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 *(x-y) + 1

def draw_symmetric(x, y, xc, yc):
    glBegin(GL_POINTS)
    glVertex2i(x + xc, y + yc)
    glVertex2i(-x + xc, y + yc)
    glVertex2i(x + xc, -y + yc)
    glVertex2i(-x + xc, -y + yc)
    glVertex2i(y + xc, x + yc)
    glVertex2i(-y + xc, x + yc)
    glVertex2i(y + xc, -x + yc)
    glVertex2i(-y + xc, -x + yc)
    glEnd()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    
r = int(input("Radius of circle: "))
x = list(map(int, input("Coordinates for center of circle:").split()))

glfw.init()
width = 500
height = 500
window = glfw.create_window(width, height, "Mid-Point Algorithm for Circle", None, None)
glfw.make_context_current(window)
while not glfw.window_should_close(window):
    render()
    draw_circle(r, x[0], x[1])
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()