import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from te import TE
import matplotlib as mpl

mpl.rcParams['font.family'] = 'simhei'
mpl.rcParams['axes.unicode_minus'] = False

origin_data = pd.read_csv('data/dataset.csv', names=['days', 'predator', 'prey'])

data_array = origin_data.values

#prey = data_array[:,1]
#predator = data_array[:,2]

prey = np.random.random(100)
predator = np.random.random(100)

x = np.array(range(1,1000))*0.001
y = list(range(1,1000))
for i in range(len(x)) :
	print(i)
	a = TE(prey, predator)
	#y[i] = a.te12()-a.te21()
	y[i] = a.kde_te12(x[i]) - a.kde_te21(x[i])

plt.plot(x,y,'r-o')
#plt.plot([5,100],[0,0],'k-')
plt.xlabel("直方图格子数")
plt.ylabel("互信息")
plt.title("随机序列之间的互信息")
'''
fig = plt.figure()
axe = fig.add_subplot(111)
axe.plot(range(100),prey,'-*',range(100),predator,'-o')
axe.set_xlabel("序号")
axe.set_ylabel("数值")
axe.set_title("随机序列")
axe.axis([-10,110,-1,2])
fig.show()
'''
plt.show()