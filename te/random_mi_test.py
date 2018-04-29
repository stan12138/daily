import numpy as np
from matplotlib import pyplot as plt
from te import TE
import pandas as pd

'''
x = np.random.random(100)
y = np.random.random(100)

fig = plt.figure(1)

ax = fig.add_subplot(111)

ax.plot(range(100),x,range(100),y)

fig2 = plt.figure(2)

ax1 = fig2.add_subplot(111)

a = TE(x, y)

m = list(range(2,100))
mi = list(range(2,100))

for i in range(len(m)) :
	print(i)
	mi[i] = a.mi(num=m[i])

ax1.plot(m, mi)

plt.show()
'''
data = pd.read_csv("data/data1/3_11.csv", names=['s1','s2'])
data = data.values
x = np.random.random(10000)
y = np.random.random(10000)
a = TE(data[:,0], data[:,1])
b = TE(x, y)
m = list(range(2,2000))
mi = list(range(2,2000))
for i in range(len(m)) :
	print('\r'+str(i),end='')
	mi[i] = a.discrete_mi(num=m[i])
	#print(mi[i])


plt.plot(m,mi)
#print(m,mi)
plt.show()