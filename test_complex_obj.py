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
from camera import Camera
from obj_loader import ObjLoader
from texture_loader import TextureLoader



ctr = False
left = False



def key_handler(window,key,scancode,action,mode) :
	#print(key,action)

	if key == 341 and action == glfw.PRESS :
		ca.set_ctr(True)
	if key == 341 and action == glfw.RELEASE :
		ca.set_ctr(False)
def scroll_handler(window,xoffset,yoffset) :
	ca.scroll(yoffset)
	
def mouse_button_handler(window,button,action,mods) :

	if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS :
		ca.set_mouse_left(True)
	elif  button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE :
		ca.set_mouse_left(False)
		
def mouse_move_handler(window,xpos,ypos) :
	ca.mouse_loc(xpos,ypos)


ca = Camera()

def main() :
	
    	
	if not glfw.init() :
		return
	window = glfw.create_window(600,600,'my window',None,None)
	if not window :
		glfw.terminate()
		return
	glfw.make_context_current(window)
	
	
	glfw.set_key_callback(window,key_handler)
	glfw.set_scroll_callback(window,scroll_handler)
	glfw.set_mouse_button_callback(window,mouse_button_handler)
	glfw.set_cursor_pos_callback(window,mouse_move_handler)
	

	shader = My_shader('cube_v.vs','cube_f.frags')
	shader.use()
	
	vb = pyrr.matrix44.create_from_y_rotation(radians(-50))
	model = pyrr.matrix44.create_from_x_rotation(radians(50))
	view = pyrr.matrix44.create_from_translation(array([0,0,-4]))
	projection = pyrr.matrix44.create_perspective_projection_matrix(60,1,0.1,100)
	
	
	cube = ObjLoader('model/model.obj')

	
	vao = glGenVertexArrays(1)
	vbo = glGenBuffers(1)
	ebo = glGenBuffers(1)

	glBindVertexArray(vao)
	glBindBuffer(GL_ARRAY_BUFFER,vbo)
	glBufferData(GL_ARRAY_BUFFER,cube.size,cube.model,GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,0,ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)
	glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(cube.vert_start))
	glEnableVertexAttribArray(1)

	
	#glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
	#glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
	glBindVertexArray(0)


	'''
	texture1 = TextureLoader('textures/wall.jpg')
	texture2 = TextureLoader('textures/smile.png',active=GL_TEXTURE1)
	
	glUniform1i(glGetUniformLocation(shader.shader,'te'),0)
	glUniform1i(glGetUniformLocation(shader.shader,'te1'),1)	
	'''
	
	
	
	
	m_loc = glGetUniformLocation(shader.shader,'model')
	glUniformMatrix4fv(m_loc,1,GL_FALSE,model)
	
	my_loc = glGetUniformLocation(shader.shader,'modely')
	glUniformMatrix4fv(my_loc,1,GL_FALSE,vb)
	
	v_loc = glGetUniformLocation(shader.shader,'view')
	glUniformMatrix4fv(v_loc,1,GL_FALSE,view)
	
	p_loc = glGetUniformLocation(shader.shader,'projection')
	glUniformMatrix4fv(p_loc,1,GL_FALSE,projection)
	

	
	glClearColor(0.2,0.3,0.2,1.0)
	glEnable(GL_DEPTH_TEST)
	


	#glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
	
	start = time()
	while not glfw.window_should_close(window) :
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		#model = pyrr.matrix44.create_from_x_rotation(radians((time()-start)*10))
		v_loc = glGetUniformLocation(shader.shader,'view')
		glUniformMatrix4fv(v_loc,1,GL_FALSE,ca.get_matrix())

		glBindVertexArray(vao)
		glDrawArrays(GL_TRIANGLES, 0, cube.triangle_num);
		glBindVertexArray(0)

		glfw.swap_buffers(window)
		
	glfw.terminate()
	
	
if __name__ == "__main__" :
	main()
    