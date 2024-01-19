import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

from helpers import altList, toNVC


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


RESOLUTION = 800
transformY = np.matrix(
    f"""{np.cos((np.pi / 180) * 40)},
0.0,
{np.sin(-(np.pi / 180) * 40)},
0.0;
0.0,
1.0,
0.0,
0.0;
{np.sin((np.pi / 180) * 40)},
0.0,
{np.cos((np.pi / 180) * 40)},
0.0;
0.0,
0.0,
0.0,
1.0"""
)

transformX = np.matrix(
    f""" 1.0,
          0.0,
          0.0,
          0.0;
          0.0,
          {np.cos((np.pi / 180) * -50)},
          {np.sin((np.pi / 180) * -50)},
          0.0;
          0.0,
          {np.sin(-(np.pi / 180) * -50)},
          {np.cos((np.pi / 180) * -50)},
          0.0;
          0.0,
          0.0,
          0.0,
          1.0"""
)
# new transformation to be applied
newTransform = np.matrix(
    f""" 1.0,
        0.0,
        0.0,
        0.0;
        0.0,
        1.0,
        0.0,
        0.0;
        0.0,
        0.0,
        1.0,
        0.0;
        0.2,
        0.2,
        0.2,
        1.0"""
)
transformation = np.dot(newTransform, np.dot(transformX, transformY))


def main(transformation):

    vertex_src = """
  #version 330 

  layout(location=0) in vec3 aPos;
  layout(location=1)  in  vec3 aColor;
  
  out vec3 vColor;
    
  uniform mat4 transformation;

  void main(){
      gl_Position = transformation * vec4(aPos,1.0);
      vColor=aColor;
  
      }
  """

    fragment_src = """
  #version 330 
  in vec3 vColor;

  out vec4 FragColor;

  void main(){
      FragColor = vec4(vColor,0.8f);
    
  }
  """

    if not glfw.init():
        raise Exception("glfw can not be initialized!")

    window = glfw.create_window(RESOLUTION, RESOLUTION, "LAB4", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    glfw.set_window_pos(window, 100, 100)
    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    vertices = [
        -0.5,
        -0.5,
        0.5,
        0.5,
        -0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        -0.5,
        0.5,
        0.5,
        -0.5,
        -0.5,
        -0.5,
        0.5,
        -0.5,
        -0.5,
        0.5,
        0.5,
        -0.5,
        -0.5,
        0.5,
        -0.5,
    ]

    colors = [
        0.0,
        0.0,
        0.0,
        
        1.0,
        0.8,
        0.0,
        
        0.0,
        0.5,
        0.0,
        
        1.0,
        0.0,
        0.5,
        
        0.8,
        0.5,
        0.5,
        
        0.0,
        0.8,
        0.5,
        
        0.0,
        0.8,
        0.0,
        
        1.0,
        0.6,
        0.0,
    ]

    indices = [
        0,
        1,
        2,
        2,
        3,
        0,
        4,
        5,
        6,
        6,
        7,
        4,
        4,
        5,
        1,
        1,
        0,
        4,
        6,
        7,
        3,
        3,
        2,
        6,
        5,
        6,
        2,
        2,
        1,
        5,
        7,
        4,
        0,
        0,
        3,
        7,
    ]

    bufferData = vertices + colors

    vertices = np.array(vertices, dtype=np.float32)
    bufferData = np.array(bufferData, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER),
    )

    vertex_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(GL_ARRAY_BUFFER, bufferData.nbytes, bufferData, GL_STREAM_DRAW)

    element_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STREAM_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(vertices.nbytes))

    glUseProgram(shader)
    transformation_location = glGetUniformLocation(shader, "transformation")

    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):

        glfw.poll_events()
        glClear(GL_DEPTH_BUFFER_BIT)
        glUniformMatrix4fv(transformation_location, 1, GL_FALSE, transformation)
        # glUniformMatrix4fv(transformation_location,1,GL_FALSE,transformation)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

main(transformation)
