import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

width = 1000
height = 1000

#Global variables
polygon_vertices = np.array([
    [400, 400],
    [800, 400],
    [800, 800],
    [400, 800]
])

x0, y0 = 600, 600

tx, ty = 200, 200
sx, sy = 1.25, 1.25
theta = 45.0
shx, shy = 2.0, 2.0

translate_factor = np.array([10,0])

def draw_polygon(polygon):
    glBegin(GL_POLYGON)
    for vertex in polygon:
        glVertex2f(vertex[0], vertex[1])
    glEnd()

#Simple Modules
def translate(tx, ty, vertices):
    vertices[0] += tx
    vertices[1] += ty
    return vertices

def rotate(theta, vertices):
    vertices[0] = vertices[0] * np.cos(np.radians(theta)) - vertices[1] * np.sin(np.radians(theta))
    vertices[1] = vertices[0] * np.sin(np.radians(theta)) + vertices[1] * np.cos(np.radians(theta))
    return vertices

def scale(sx, sy, vertices):
    vertices[0] = sx * vertices[0]
    vertices[1] = sy * vertices[1]
    return vertices

def shear(shx, shy, vertices):
    temp = vertices[0]
    vertices[0] += shx * vertices[1]
    vertices[1] += shy * temp
    return vertices

def reflection(along, vertices):
    if along == 1:
        vertices[0] = vertices[0]
        vertices[1] = -vertices[1]
    elif along == 2:
        vertices[0] = -vertices[0]
        vertices[1] = vertices[1]
    elif along == 3:
        vertices[0] = vertices[1]
        vertices[1] = vertices[0]
    else:
        print("Envalid input:")
    return vertices


def which_step(no, vertices, along):
    if no == 1:
        return translate(tx, ty, vertices)
    elif no == 2:
        return rotate(theta, vertices)
    elif no == 3:
        return scale(sx, sy, vertices)
    elif no == 4:
        return shear(shx, shy, vertices)
    elif no == 5:
        return reflection(along, vertices)

def simple_tranformation(num, res_arr, along):
    dummy = polygon_vertices.copy()
    for vertices in dummy:
        vertices[0] -= x0
        vertices[1] -= y0
    for i in range(num):
        for vertices in dummy:
            vertices = which_step(res_arr[i], vertices, along)
    for vertices in dummy:
        vertices[0] += x0
        vertices[1] += y0
    return dummy
#Composite Matrics Modules

def user_input():
    num = int(input(("Number of transformations.")))
    arr_transformation = [0 for i in range (num)]
    for i in range(num):
        print("1. Translation\n2. Rotation\n3. Scale\n4. Shear\n5. Reflection")
        arr_transformation[i] = int(input())
    r_type = int(input("Type of reflection:\n1 for along x-axis.\n2 for along y-axis.\n3 for along x=y.\n"))
    print(arr_transformation)
    print(r_type)
    
    return arr_transformation, r_type, num


base_translate_1 = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]])
base_translate_2 = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]])
translation_matrix = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
rotation_matrix = np.array([[np.cos(np.radians(theta)), -np.sin(np.radians(theta)), 0],
                            [np.sin(np.radians(theta)), np.cos(np.radians(theta)), 0],
                            [0, 0, 1]])
scaling_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
shearing_matrix = np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]])
reflection_matrix = np.empty_like(shearing_matrix)



def ref_mat_calc(along):
    r_matrix = np.array([[],[],[]])
    if (along == 1):
        r_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif (along == 2):
        r_matrix = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif (along == 3):
        r_matrix = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    else:
        print("Envalid input:")
    return r_matrix

# Transformation matrices

#Relate array to type
def which(no):
    if no == 1:
        return translation_matrix
    elif no == 2:
        return rotation_matrix
    elif no == 3:
        return scaling_matrix
    elif no == 4:
        return shearing_matrix
    elif no == 5:
        return reflection_matrix

#Give off composite matrix
def comp_composite(num, res_arr):
    composite_matrix = base_translate_2.copy()
    for i in range(num):
        composite_matrix = np.dot(which(res_arr[i]),composite_matrix)
    composite_matrix = np.dot(base_translate_1, composite_matrix)
    return composite_matrix

def transform_composite(composite_matrix, x, y):
    original = np.array([x, y, 1])
    transformed = np.dot(composite_matrix, original)
    return transformed[0], transformed[1]

def transformed_matrix_calculation(polygon, composite_matrix):
    dummy = polygon.copy()
    for points in dummy:
        points[0], points[1] = transform_composite(composite_matrix, points[0], points[1])
    return dummy
    
    
def display(x,y):
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Original in red
    glColor3f(1,0,0 )
    draw_polygon(x)
    
    #Transformed in green
    glColor3f(0, 1, 0)
    draw_polygon(y)
    
    glFlush()


def render(x,y):
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    display(x,y)

def composite_method():
    print("--------------- COMPOSITE TRANSFORAMTION ---------------")
    t_array, r_type, num = user_input()
    reflection_matrix = ref_mat_calc(r_type)
    composite_transformation_matrix = comp_composite(num, t_array)
    transformed_polygon = transformed_matrix_calculation(polygon_vertices, composite_transformation_matrix)
    
    glfw.init()

    window = glfw.create_window(width, height, "Composite Transformation", None, None)
    glfw.make_context_current(window)
    while not glfw.window_should_close(window):

        render(polygon_vertices, transformed_polygon)
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
            glfw.set_window_should_close(window, True)
        glfw.poll_events()
        glfw.swap_buffers(window)
    glfw.terminate()

def simple_method():
    
    print("--------------- Simple TRANSFORAMTION ---------------")
    t_array, r_type, num = user_input()
    transformed_polygon= simple_tranformation(num, t_array, r_type)
    
    
    glfw.init()

    window = glfw.create_window(width, height, "Simple Transformation", None, None)
    glfw.make_context_current(window)
    while not glfw.window_should_close(window):

        render(polygon_vertices, transformed_polygon)
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
            glfw.set_window_should_close(window, True)
        glfw.poll_events()
        glfw.swap_buffers(window)
    glfw.terminate()

#composite_method()
simple_method()







