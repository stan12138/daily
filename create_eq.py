from matplotlib import pyplot as plt
from random import choice
from numpy import array
import matplotlib

__all__=['create']

def create(aim,size=35,name=None,name_pre=None) :
	pad = array([[-5,-5],[5,5]])
	namelist=list(range(65,123))   #用于自动创建图片名字
	if type(aim)==str :
		fig = plt.figure()
		text = fig.text(0.5,0.5,aim,fontsize=size,ha='center',va='center')   #注意居中
		#plt.show()
		box = text.get_window_extent(fig.canvas.get_renderer())   #这句就是精华所在，在text的所有属性中，只有window_extent可以提供位置矩形坐标，但是要产生这个属性必须渲染
		#你要么选择plt.show()让系统自动渲染，但是这个打开的图片，命令很难自动关闭，用户体验极差，我们可以传入一个renderer，让它不显示而实现渲染
		#这个答案来自stackoverflow问题：matplotlib:get text bounding box, independent of backend
		#plt.close()
		point = box.get_points()+pad    #对于拿到的box，points属性包含了一个numpy的array数组，是左下右上角坐标，不包含padding，所以要手动加一点padding
		bbox = matplotlib.transforms.Bbox(point/fig.dpi)   #我们需要对拿到的box做处理，生成一个inche格式的坐标
		if name :
			fig.savefig(name,format='png',transparent=True,bbox_inches=bbox,dpi=600)  #这一句里面的bbox-inches是精华，它可以保存figure里面指定的部分，但要求是英寸，至此完美结束
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
			point = box.get_points()+pad
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