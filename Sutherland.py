import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

x_min, y_min, x_max, y_max = 50, 50, 200, 200
polygon = [(0, 75), (150, 150), (50, 150)]

def inside(x, y, edge):
    x1, y1, x2, y2 = edge
    return (x2 - x1) * (y - y1) > (y2 - y1) * (x - x1)

def compute_intersection(x1, y1, x2, y2, edge):
    x3, y3, x4, y4 = edge
    ix = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 -y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    iy = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 -y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    return ix, iy

def sutherland_hodgman():
    global polygon
    result = []
    clip_edges = [(x_min, y_min, x_max, y_min), (x_max, y_min,x_max, y_max),(x_max, y_max, x_min, y_max), (x_min, y_max, x_min, y_min)]
    for edge in clip_edges:
        result = []
        prev_vertex = polygon[-1]
    for vertex in polygon:
        if inside(*vertex, edge):
            if not inside(*prev_vertex, edge):
                result.append(compute_intersection(*prev_vertex, *vertex, edge))
            result.append(vertex)
        elif inside(*prev_vertex, edge):
            result.append(compute_intersection(*prev_vertex,*vertex, edge))
        prev_vertex = vertex
    polygon = result.copy()
            
def draw_polygon(vertices, color):
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x_min, y_min)
    glVertex2f(x_max, y_min)
    glVertex2f(x_max, y_max)
    glVertex2f(x_min, y_max)
    glEnd()
    draw_polygon(polygon, (1.0, 0.0, 0.0))
    sutherland_hodgman()
    draw_polygon(polygon, (0.0, 1.0, 0.0))
    glFlush()
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    display()

glfw.init()

width = 400
height = 400

window = glfw.create_window(width, height, "Sutherland", None, None)
glfw.make_context_current(window)

render()

while not glfw.window_should_close(window):
    
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()