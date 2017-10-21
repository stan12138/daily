# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 11:06:35 2017

@author: Stan
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

ctr = False
left = False



def key_handler(window,key,scancode,action,mode) :
	#print(key,action)
	global ctr
	if key == 341 and action == glfw.PRESS :
		ctr = True
	if key == 341 and action == glfw.RELEASE :
		ctr = False
def scroll_handler(window,xoffset,yoffset) :
	print(xoffset,yoffset)
	
def mouse_button_handler(window,button,action,mods) :
	global left
	if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS :
		left = True
	elif  button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE :
		left = False
		
def mouse_move_handler(window,xpos,ypos) :
	print(xpos,ypos)
def main():

	# initialize glfw
	if not glfw.init():
		return

	window = glfw.create_window(800, 600, "My OpenGL window", None, None)

	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)
	glfw.set_key_callback(window,key_handler)
	glfw.set_scroll_callback(window,scroll_handler)
	glfw.set_mouse_button_callback(window,mouse_button_handler)
	glfw.set_cursor_pos_callback(window,mouse_move_handler)


	glClearColor(0.2, 0.3, 0.2, 1.0)

	while not glfw.window_should_close(window):
		glfw.poll_events()

		glClear(GL_COLOR_BUFFER_BIT)

		glfw.swap_buffers(window)

	glfw.terminate()

if __name__ == "__main__":
	main()