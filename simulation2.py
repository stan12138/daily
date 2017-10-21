import numpy as np
from math import log2
from matplotlib import pyplot as plt
#e = 0.03


def f(a,b,e) :
	x = e*a + (1-e)*b
	x = x.flatten()
	r = x[:]
	x[r<0.5] = 2*x[r<0.5]
	x[r>=0.5] = 2-2*x[r>=0.5]
	'''
	if x<0.5 :
		return 2*x
	else :
		return 2-2*x
	'''
#record = np.array([100,10000],dtype=np.float64)

def onetime(e) :
	record = np.zeros([100,10000], dtype=np.float64)
	origin = np.random.random([100,1]).flatten()

	for i in range(100000) :
		#origin[0] = f(origin[0], origin[0], e)
		a = origin[:-1]
		b = origin[1:]
		c = f(a, b, e)
		origin[0] = f(origin[0], origin[0], e)
		origin[1:] = c
		'''
		for j in range(1,100) :
			new1 = f(origin[j-1,0], origin[j,0], e)
			origin[j-1,0] = new
			new = new1
		origin[j,0] = new
		'''
	record[:,0] = origin[:]
	for i in range(1,10000) :
		a = record[:-1,i-1]
		b = record[1:,i-1]
		c = f(a, b, e)
		record[0,i] = f(record[0,i-1], record[0,i-1], e)
		record[1:,i] = c
		'''
		for j in range(1,100) :
			record[j,i] = f(record[j-1,i-1], record[j,i-1], e)
		'''
	last2 = record[-2:,:]

	Nxn1xnyn = {'000':0,'001':0,'010':0,'011':0,'100':0,'101':0,'110':0,'111':0}
	Nxn = {'0':0,'1':0}
	Nxnyn = {'00':0,'01':0,'10':0,'11':0}
	Nxn1xn = {'00':0,'01':0,'10':0,'11':0}

	for i in range(1,10000) :
		xn1, xn, yn = '0','0','0'
		if last2[0,i-1] >= 0.5 :
			yn = '1'
		if last2[1,i-1] >= 0.5 :
			xn = '1'
		if last2[1,i] >= 0.5 :
			xn1 = '1'
		Nxn1xnyn[xn1+xn+yn] += 1
		Nxn[xn] += 1
		Nxnyn[xn+yn] += 1
		Nxn1xn[xn1+xn] += 1
	res = 0
	for i in ('0','1') :
		for j in ('0','1') :
			for k in ('0','1') :
				if not Nxnyn[j+k]*Nxn1xn[i+j] == 0 :
					res += Nxn1xnyn[i+j+k]*log2((Nxn1xnyn[i+j+k]*Nxn[j])/(Nxnyn[j+k]*Nxn1xn[i+j]))

	return res/9999

e = np.array(range(10), dtype=np.float64)
e = e*0.005
t = np.array(range(10), dtype=np.float64)
t = t*0
for times in range(1) :
	for i in range(10) :
		print(i)
		t[i] += onetime(e[i])
t = t
plt.plot(e,t,'r-*')
plt.show()