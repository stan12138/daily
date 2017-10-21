# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:50:10 2017

@author: stan han
"""
__all__ = ['My_shader']

from OpenGL.GL import *
import OpenGL.GL.shaders


class My_shader:
    
    def __init__(self,v_path,f_path) :
        
        with open(v_path,'r') as v_file :
            v_source = v_file.read()


        with open(f_path,'r') as f_file :
            f_source = f_file.read()


        v_shader = OpenGL.GL.shaders.compileShader(v_source,GL_VERTEX_SHADER)
        f_shader = OpenGL.GL.shaders.compileShader(f_source,GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(v_shader, f_shader)

    def use(self) :
        glUseProgram(self.shader)

    def setvec3(self,name,a,b,c) :
        loc = glGetUniformLocation(self.shader,name)
        glUniform3f(loc,a,b,c)


     