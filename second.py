# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:05:10 2017

@author: stan han
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL.GL
from numpy import array,float32,uint8,uint32,pi
from shader_loader import My_shader
from PIL import Image

def main() :
    
    if not glfw.init() :
        return
    window = glfw.create_window(600,600,'my window',None,None)
    if not window :
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    point = array([-0.5,0.5,0,0,1,   0.5,0.5,0,1,1,  0.5,-0.5,0,1,0,  -0.5,-0.5,0,0,0],dtype=float32)
    index = array([0,1,2,2,3,0],dtype=uint32)
    shader = My_shader('v.vs','f.frags')
    shader.use()
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
    
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    image = Image.open('textures/wall.jpg')
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    
    #image = array(image,dtype=uint8)
    height,width= image.height,image.width
    
    image = image.tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,5*4,ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,5*4,ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    
    glClearColor(0.2,0.3,0.2,1.0)
    #glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    
    while not glfw.window_should_close(window) :
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
    
if __name__ == "__main__" :
    main()
        
        
        