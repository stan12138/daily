# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 13:09:45 2017

@author: Stan
"""
import numpy as np
from math import sin,cos,radians
import pyrr

def my_normalize(a) :
	return a/sum(a**2)

class Camera :
	def __init__(self) :
		self.forward = np.array([0,0,-1],dtype=np.float32)
		self.right = np.array([1,0,0],dtype=np.float32)
		self.up = np.array([0,1,0],dtype=np.float32)
		
		self.pos = np.array([0,0,0],dtype=np.float32)
		self.yaw = 0
		self.pitch = 0
		
		self.ctr = False
		self.mouse_left = False
		
		self.oldx = -100
		self.oldy = -100
		
		self.v = 0.01
		
	def update(self) :
		self.forward[0] = -sin(radians(self.yaw))*cos(radians(self.pitch))
		self.forward[1] = sin(radians(self.pitch))
		self.forward[2] = -cos(radians(self.yaw))*cos(radians(self.pitch))
		
		self.right[0] = cos(radians(self.yaw))
		self.right[1] = 0
		self.right[2] = -sin(radians(self.yaw))
		
		self.up = my_normalize(np.cross(self.right,self.forward))
		
	def mouse_loc(self,xpos,ypos) :
		if self.ctr :
			if self.oldx>-1 :
				self.yaw += self.v*5*(xpos-self.oldx)
				self.pitch -= self.v*5*(self.oldy-ypos)
				
				self.yaw = min(max(self.yaw,-90),90)
				self.pitch = min(max(self.pitch,-90),90)
				self.oldx = xpos
				self.oldy = ypos
				self.update()
			else :
				self.oldx = xpos
				self.oldy = ypos
				
		elif self.mouse_left :
			if self.oldx>-1 :
				self.pos -= self.v*(self.oldy-ypos)*self.up
				self.pos -= self.v*(xpos-self.oldx)*self.right
				self.oldx = xpos
				self.oldy = ypos				
				
			else :
				self.oldx = xpos
				self.oldy = ypos
			
			
	
	def set_ctr(self,value) :
		self.ctr = value
		if not value :
			self.oldx = -100
		
	def set_mouse_left(self,value) :
		self.mouse_left = value
		if not value :
			self.oldx = -100
		
	def scroll(self,ypos) :
		self.pos += 0.5*ypos*self.forward
		
	def get_matrix(self) :
		 return pyrr.matrix44.create_look_at(self.pos,self.pos+self.forward,self.up)
		
		
if __name__ == '__main__' :
	ca = Camera()
	ca.update()
	print(ca.up,ca.forward,ca.right)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	