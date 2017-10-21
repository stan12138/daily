import glfw
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders

def main() :
    if not glfw.init() :
        return
    
    window = glfw.create_window(800,600,"stan's first example",None,None)
    
    if not window :
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    vertex = [
             0.5, 0.5, 0.0,  1.0,0.0,0.0,
            -0.5, 0.5, 0.0,  0.0,1.0,0.0,
            -0.5,-0.5, 0.0,  1.0,0.0,0.0,
             0.5,-0.5, 0.0,  0.0,1.0,0.0
            ]
    
    index = [0,1,2,  2,3,0]
    
    vertex = np.array(vertex,dtype=np.float32)
    index = np.array(index,dtype=np.uint32)    #此处绝对不能使用GLSL中没有的类型，如uint8
    
    
    v_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec4 final_color;
    
    void main()
    {
       gl_Position = vec4(position,1.0f);
       final_color = vec4(color,1.0f);
    }
    """
    
    f_shader = '''
    #version 330
    in vec4 final_color;
    
    out vec4 f_color;
    
    void main()
    {
       f_color = final_color;
    }
    '''
    vertex_shader = OpenGL.GL.shaders.compileShader(v_shader, GL_VERTEX_SHADER)
    fragment_shader = OpenGL.GL.shaders.compileShader(f_shader, GL_FRAGMENT_SHADER)
    shader = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)
    
    
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)
    
    glBindBuffer(GL_ARRAY_BUFFER,VBO)
    glBufferData(GL_ARRAY_BUFFER,4*len(vertex),vertex,GL_STATIC_DRAW)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
    
    
    position = glGetAttribLocation(shader,'position')
    glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shader,'color')
    glVertexAttribPointer(color,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
    
    
    glUseProgram(shader)
    glClearColor(0.2,0.3,0.2,1.0)
    
    while not glfw.window_should_close(window) :
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
        
        glDrawElements(GL_LINE_LOOP,6,GL_UNSIGNED_INT,None)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
    
if __name__ == '__main__' :
    main()
    