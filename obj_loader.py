import numpy as np

__all__ = ['ObjLoader']

class ObjLoader :
	def __init__(self,path) :
		self.vertex = []
		self.tex_coords = []
		self.normals = []

		self.vertex_index = []
		self.tex_index = []
		self.normal_index = []

		self.has_normal = False

		self.model = []
		self.load(path)
		

	def load(self,path,dtype=np.float32) :

		with open(path,'r') as fi :
			content = fi.readlines()

		for line in content :
			if line.startswith('#') :
				continue
			values = line.split()
			if not values :
				continue
			if values[0] == 'v' :
				self.vertex.append(values[1:4])
			elif values[0] == 'vt' :
				self.tex_coords.append(values[1:3])
			elif values[0] == 'vn' :
				self.normals.append(values[1:4])
			elif values[0] == 'f' :
				face = []
				tex = []
				normal = []

				for va in values[1:4] :
					val = va.split('/')
					self.vertex_index.append(int(val[0])-1)
					self.tex_index.append(int(val[1])-1)
					if len(val)==3 :
						self.normal_index.append(int(val[2])-1)
						self.has_normal = True

		self.model.extend([valu for i in self.vertex_index for valu in self.vertex[i]])
		self.model.extend([valu for i in self.tex_index for valu in self.tex_coords[i]])
		if self.has_normal :
			self.model.extend([valu for i in self.normal_index for valu in self.normals[i]])

		self.model = np.array(self.model,dtype=dtype)

		self.vert_start = 0
		self.tex_start = len(self.vertex_index)*3*4
		self.normal_start = (len(self.vertex_index)*3+len(self.tex_index)*2)*4
		self.size = self.model.itemsize*len(self.model)
		self.triangle_num = len(self.vertex_index)
if __name__ == '__main__' :
	test = ObjLoader('cube.obj')
	print(test.model)
	print(test.vert_start)
	print(test.tex_start)
	print(test.normal_start)
	print(test.size)

