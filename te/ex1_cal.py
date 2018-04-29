import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from te import TE
import matplotlib as mpl
import pickle
import time

start = time.time()
mpl.rcParams['font.family'] = 'simhei'
mpl.rcParams['axes.unicode_minus'] = False
res = np.zeros(26, dtype=np.float)
for i in range(10) :
	for j in range(1,26) :
		#print(i,j)
		data = pd.read_csv("data/data1/"+str(i)+'_'+str(j)+'.csv', names=['s1','s2'])
		data = data.values
		a = TE(data[:,0], data[:,1])
		res[j] += a.discrete_te12(num=2)
res /= 10

e = np.array(range(26),dtype=np.float32)
e = e*0.002
res1 = 0.77**2*(e**2)/np.log(2)
d1 = [0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032, 0.034, 0.036, 0.038, 0.04, 0.042, 0.044, 0.046, 0.048]
d2 = [0.00031925,  0.00037872,  0.00044757,  0.00056651,  0.0007011,0.00070736,  0.00081064,  0.00086698,  0.0010266,  0.00121127, 0.00123005,  0.00146479,  0.00168701,  0.00182473,  0.00207825]


p1 = 10
p2 = 24
print(p1,p2)
my_res = res[p1:p2+1]
th_res = res1[p1:p2+1]


pa_pan = np.abs(d2-th_res)
my_pan = np.abs(my_res-th_res)

my_j = np.sum(my_pan)/len(my_pan)
pa_j = np.sum(pa_pan)/len(pa_pan)

my_f = np.sum((my_pan-my_j)**2)/len(my_pan)
pa_f = np.sum((pa_pan-pa_j)**2)/len(pa_pan)

print("论文中的偏差,我的偏差")
print(pa_pan,my_pan)

print("论文中的偏差均值,我的偏差均值")
print(pa_j,my_j)

print("论文中的偏差方差,我的偏差方差")
print(pa_f,my_f)



line1 = plt.plot(e,res,'-*', label="计算值")
line2 = plt.plot(e,res1,'-*',label="理论值")
line3 = plt.plot(d1,d2,'r-o',label="论文中计算值")

plt.legend()
plt.xlabel("耦合系数")
plt.ylabel("传输熵")
plt.title("论文例1计算对比")
print("work done with %s minutes"%((time.time()-start)/60))
plt.show()
