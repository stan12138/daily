# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:15:42 2017

@author: Stan
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL.GL
from numpy import array,float32,uint8,uint32,pi
from shader_loader import My_shader
from PIL import Image
import pyrr
from math import radians
from time import time


def main() :
	
	
	if not glfw.init() :
		return
	window = glfw.create_window(600,600,'my window',None,None)
	if not window :
		glfw.terminate()
		return
	glfw.make_context_current(window)
	point = [
        -0.5, -0.5, 0.5, 0.0, 0.0, 0.0, 0.0,1.0,    
        0.5, -0.5, 0.5, 1.0, 0.0,  0.0, 0.0, 1.0,   
        0.5, 0.5, 0.5,  1.0, 1.0,   0.0, 0.0, 1.0,  
        0.5, 0.5, 0.5,  1.0, 1.0,   0.0, 0.0, 1.0,  
        -0.5, 0.5, 0.5,  0.0, 1.0,  0.0, 0.0, 1.0,  
        -0.5, -0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0,   
        

        -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, -1.0, 
        -0.5, 0.5, -0.5,  0.0, 1.0,  0.0, 0.0, -1.0, 
        0.5, 0.5, -0.5,   1.0, 1.0, 0.0, 0.0, -1.0, 
        0.5, 0.5, -0.5,   1.0, 1.0, 0.0, 0.0, -1.0, 
        0.5, -0.5, -0.5,  1.0, 0.0, 0.0, 0.0, -1.0, 
        -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, -1.0, 

        -0.5, 0.5, 0.5, 0.0, 1.0,   -1.0, 0.0, 0.0, 
        -0.5, 0.5, -0.5, 1.0, 1.0,   -1.0, 0.0, 0.0, 
        -0.5, -0.5, -0.5, 1.0, 0.0, -1.0, 0.0, 0.0, 
        -0.5, -0.5, -0.5,1.0, 0.0, -1.0, 0.0, 0.0,  
        -0.5, -0.5, 0.5, 0.0, 0.0,  -1.0, 0.0, 0.0, 
        -0.5, 0.5, 0.5, 0.0, 1.0,   -1.0, 0.0, 0.0, 

        0.5, -0.5, -0.5,1.0, 0.0, 1.0, 0.0, 0.0, 
        0.5, 0.5, -0.5,1.0, 1.0,  1.0, 0.0, 0.0, 
        0.5, 0.5, 0.5,0.0, 1.0,   1.0, 0.0, 0.0, 
        0.5, 0.5, 0.5,0.0, 1.0,   1.0, 0.0, 0.0, 
        0.5, -0.5, 0.5,0.0, 0.0,  1.0, 0.0, 0.0, 
        0.5, -0.5, -0.5,1.0, 0.0, 1.0, 0.0, 0.0, 

        0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 1.0, 0.0,    
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0,    
        -0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0,    
        -0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0,    
        0.5, 0.5, 0.5,  1.0, 0.0,  0.0, 1.0, 0.0,   
        0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 1.0, 0.0,    

        -0.5, -0.5, 0.5,0.0, 0.0,  0.0, -1.0, 0.0,  
        -0.5, -0.5, -0.5,0.0, 1.0, 0.0, -1.0, 0.0,  
        0.5, -0.5, -0.5, 1.0, 1.0,  0.0, -1.0, 0.0, 
        0.5, -0.5, -0.5, 1.0, 1.0,  0.0, -1.0, 0.0, 
        0.5, -0.5, 0.5, 1.0, 0.0,   0.0, -1.0, 0.0, 
        -0.5, -0.5, 0.5, 0.0, 0.0,  0.0, -1.0, 0.0]#顶点，纹理坐标，法向量
	point = array(point,dtype=float32)
	#point = array([-0.5,0.5,0,1,0,0,0,1,   0.5,0.5,0,0,1,0,1,1,  0.5,-0.5,0,0,0,1,1,0,  -0.5,-0.5,0,1,1,0,0,0],dtype=float32)
	
	index = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               8, 9, 10, 10, 11, 8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]
	index = array(index,dtype=uint32)
	
	#index = array([0,1,3,1,2,3],dtype=uint32)
	shader = My_shader('v.vs','f.frags')
	shader.use()
	
	vb = pyrr.matrix44.create_from_y_rotation(radians(-50))
	
	model = pyrr.matrix44.create_from_x_rotation(radians(50))
	view = pyrr.matrix44.create_from_translation(array([0,0,-4]))
	projection = pyrr.matrix44.create_perspective_projection_matrix(45,1,0.1,100)
	
	
	
	
	vbo = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER,vbo)
	glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
	
	'''
	ebo = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
	'''
	
	texture1 = glGenTextures(1)
	
	
	glActiveTexture(GL_TEXTURE0)
	glBindTexture(GL_TEXTURE_2D,texture1)
	
	image = Image.open('textures/container.jpg')
	height,width = image.height,image.width
	image = image.transpose(Image.FLIP_TOP_BOTTOM)
	image = image.convert("RGB").tobytes()
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
	glGenerateMipmap(GL_TEXTURE_2D)
	
	glBindTexture(GL_TEXTURE_2D,texture1)
	
	
	
	texture2 = glGenTextures(1)
	
	
	glActiveTexture(GL_TEXTURE1)
	glBindTexture(GL_TEXTURE_2D,texture2)
	image1 = Image.open('textures/smile.png')
	image2 = image1.transpose(Image.FLIP_TOP_BOTTOM)
	image2 = image2.convert("RGBA").tobytes()
	height,width = image1.height,image1.width
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image2)
	glGenerateMipmap(GL_TEXTURE_2D)	
	
	glBindTexture(GL_TEXTURE_2D,texture2)
	
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	

	

	
	glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)
	
	glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(12))
	glEnableVertexAttribArray(1)
	
	glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(20))
	glEnableVertexAttribArray(2)
	
	
	m_loc = glGetUniformLocation(shader.shader,'model')
	glUniformMatrix4fv(m_loc,1,GL_FALSE,model)
	
	my_loc = glGetUniformLocation(shader.shader,'modely')
	glUniformMatrix4fv(my_loc,1,GL_FALSE,vb)
	
	v_loc = glGetUniformLocation(shader.shader,'view')
	glUniformMatrix4fv(v_loc,1,GL_FALSE,view)
	
	p_loc = glGetUniformLocation(shader.shader,'projection')
	glUniformMatrix4fv(p_loc,1,GL_FALSE,projection)
	
	
	glUniform1i(glGetUniformLocation(shader.shader,'te'),0)
	glUniform1i(glGetUniformLocation(shader.shader,'te1'),1)
	
	glClearColor(0.2,0.3,0.2,1.0)
	glEnable(GL_DEPTH_TEST)
	
	#glUniform3f(glGetUniformLocation(shader.shader,'ocolor'),1.0,0.5,0.31)
	#glUniform3f(glGetUniformLocation(shader.shader,'light'),1.0,1.0,1.0)
	
	shader.setvec3('ocolor',1.0,0.5,0.31)
	shader.setvec3('light',1.0,1.0,1.0)
	shader.setvec3('lightpos',4,4,0.5)
	shader.setvec3('viewpos',0,0,4)
	#glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
	start = time()
	while not glfw.window_should_close(window) :
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		#model = pyrr.matrix44.create_from_x_rotation(radians((time()-start)*10))
		m_loc = glGetUniformLocation(shader.shader,'model')
		glUniformMatrix4fv(m_loc,1,GL_FALSE,model)
		glDrawArrays(GL_TRIANGLES, 0, 36);
		
		glfw.swap_buffers(window)
		
	glfw.terminate()
	
	
if __name__ == "__main__" :
	main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    