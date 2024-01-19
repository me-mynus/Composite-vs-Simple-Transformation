import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

#Global variables
rectangle_vertices = [
    [100, 100],
    [100, 600],
    [600, 100],
    [600, 600]
]

x0, y0 = 300, 300

tx, ty = 0.0, 0.0
sx, sy = 2.0, 2.0
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

def rotate(degree, vertices):
    vertices[0] = vertices[0] * np.cos(np.radians(theta)) - vertices[1] * np.sin(np.radians(theta))
    vertices[1] = vertices[0] * np.sin(np.radians(theta)) + vertices[1] * np.cos(np.radians(theta))
    return vertices

def scale(sx, sy, vertices):
    vertices[0] = sx * vertices
    vertices[1] = sy * vertices
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
    
    return arr_transformation, r_type


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

def comp_composite(num, res_arr):
    composite_matrix = base_translate_2
    for i in range(num):
        composite_matrix = np.dot(which(res_arr[i]),composite_matrix)
    return composite_matrix

def transform_composite(composite_matrix, x, y):
    original = np.array([x, y, 1])
    ans = np.dot(np.dot(base_translate_1, composite_matrix), original)
    return ans


def draw_rectangle_transformed(composite_matrix):
    glBegin(GL_QUADS)
    for vertex in rectangle_vertices:
        vertex = transform_composite(composite_matrix, vertex[0], vertex[1])
        glVertex2f(vertex[0], vertex[1])
    glEnd()

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


# Function to apply transformation without using composite matrix
def apply_transform_without_composite(x, y):
    # Translation
    x -= x0
    y -= y0

    # Rotation
    x_rot = x * np.cos(np.radians(theta)) - y * np.sin(np.radians(theta))
    y_rot = x * np.sin(np.radians(theta)) + y * np.cos(np.radians(theta))

    # Scaling
    x_scale = x_rot * scale_factor
    y_scale = y_rot * scale_factor

    # Shearing
    x_shear = x_scale + y_scale * shear_factor
    y_shear = y_scale + x_scale * shear_factor

    # Translation back
    x_shear += x0
    y_shear += y0

    return x_shear, y_shear

# Function to apply transformation using composite matrix
def a1():
    point = np.array([x, y, 1])
    transformed_point = np.dot(composite_matrix, point)
    return transformed_point[0], transformed_point[1]

def main():
    t_array, r_type = user_input()
    reflection_matrix = ref_mat_calc(r_type)
    print(reflection_matrix)
    

main()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 1)

    # Apply transformation without composite matrix
    glColor3f(1, 0, 0)

    # Apply transformation with composite matrix
    glColor3f(0, 0, 1)

    glFlush()

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

window = glfw.create_window(width, height, "Ellipse Drawing", None, None)
glfw.make_context_current(window)
while not glfw.window_should_close(window):

    render()
    if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.set_window_should_close(window, True)
    glfw.poll_events()
    glfw.swap_buffers(window)
glfw.terminate()
