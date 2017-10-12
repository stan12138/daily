from matplotlib import pyplot as plt
from random import choice

__all__=['create']

def create(aim,size=35,name=None,name_pre=None) :
	namelist=list(range(65,123))
	if type(aim)==str :
		fig = plt.figure()
		fig.text(0.5,0.5,aim,fontsize=size,ha='center',va='center')
		if name :
			plt.savefig(name,format='png',transparent=True,dpi=600)
		else :
			plt.savefig(chr(choice(namelist))+chr(choice(namelist))+chr(choice(namelist))+'.png',format='png',transparent=True,dpi=600)
		plt.close()
	elif type(aim)==list or type(aim)==tuple :
		j = 0
		if not name_pre :
			name_pre = chr(choice(namelist))+chr(choice(namelist))+chr(choice(namelist))
		for i in aim :
			fig = plt.figure()
			fig.text(0.5,0.5,i,fontsize=size,ha='center',va='center')
			if name and len(name)==len(aim) :
				plt.savefig(name[j],format='png',transparent=True,dpi=600)
			else :
				plt.savefig(name_pre+str(j)+'.png',format='png',transparent=True,dpi=600)
			j += 1
			plt.close()

if __name__ == '__main__' :
	aim = [r'$s_{a}=1$',r'$a_{s}=3$']
	create(aim)