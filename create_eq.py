from matplotlib import pyplot as plt
from random import choice
from numpy import array
import matplotlib

__all__=['create']

def create(aim,size=35,name=None,name_pre=None) :
	namelist=list(range(65,123))
	if type(aim)==str :
		fig = plt.figure()
		text = fig.text(0.5,0.5,aim,fontsize=size,ha='center',va='center')
		plt.show()
		box = text.get_window_extent()
		plt.close()
		point = box.get_points()+array([[-5,-5],[5,5]])
		bbox = matplotlib.transforms.Bbox(point/fig.dpi)
		if name :
			fig.savefig(name,format='png',transparent=True,bbox_inches=bbox,dpi=600)
		else :
			fig.savefig(chr(choice(namelist))+chr(choice(namelist))+chr(choice(namelist))+'.png',format='png',bbox_inches=bbox,transparent=True,dpi=600)
		plt.close()
	elif type(aim)==list or type(aim)==tuple :
		j = 0
		if not name_pre :
			name_pre = chr(choice(namelist))+chr(choice(namelist))+chr(choice(namelist))
		for i in aim :
			fig = plt.figure()
			text = fig.text(0.5,0.5,i,fontsize=size,ha='center',va='center')
			#plt.show()
			box = text.get_window_extent(fig.canvas.get_renderer())
			#plt.close()
			point = box.get_points()+array([[-5,-5],[5,5]])
			bbox = matplotlib.transforms.Bbox(point/fig.dpi)
			if name and len(name)==len(aim) :
				fig.savefig(name[j],format='png',transparent=True,bbox_inches=bbox,dpi=600)
			else :
				fig.savefig(name_pre+str(j)+'.png',format='png',transparent=True,bbox_inches=bbox,dpi=600)
			j += 1
			plt.close()

if __name__ == '__main__' :
	aim = [r'$s_{a}=1$',r'$a_{s}=3$']
	create(aim)