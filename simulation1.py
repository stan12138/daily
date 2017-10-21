import numpy as np
from math import log2
from matplotlib import pyplot as plt
import multiprocessing
#e = 0.03

'''
def f(a,b,e) :
	x = e*a + (1-e)*b
	if x<0.5 :
		return 2*x
	else :
		return 2-2*x
'''
#record = np.array([100,10000],dtype=np.float64)

def onetime(e) :
	f = lambda aa,bb,ee: 2*(ee*aa + (1-ee)*bb) if ee*aa + (1-ee)*bb < 0.5 else 2-2*(ee*aa + (1-ee)*bb)
	record = np.zeros([100,100000], dtype=np.float64)
	origin = np.random.random([100,1])

	for i in range(100000) :
		new = f(origin[0,0], origin[0,0], e)
		for j in range(1,100) :
			new1 = f(origin[j-1,0], origin[j,0], e)
			origin[j-1,0] = new
			new = new1
		origin[j,0] = new

	record[:,0] = origin[:,0]
	for i in range(1,100000) :
		record[0,i] = f(record[0,i-1], record[0,i-1], e)
		for j in range(1,100) :
			record[j,i] = f(record[j-1,i-1], record[j,i-1], e)
	last2 = record[-2:,:]

	Nxn1xnyn = {'000':0,'001':0,'010':0,'011':0,'100':0,'101':0,'110':0,'111':0}
	Nxn = {'0':0,'1':0}
	Nxnyn = {'00':0,'01':0,'10':0,'11':0}
	Nxn1xn = {'00':0,'01':0,'10':0,'11':0}

	for i in range(1,100000) :
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

	#lock.acquire()
	return res/9999
	#lock.release()
if __name__ == '__main__' :
	e = np.array(range(50), dtype=np.float64)
	e = e*0.001

	tt = multiprocessing.Array('d',range(50))
	lock = multiprocessing.Lock()
	t = list(range(50))
	pool = multiprocessing.Pool(processes=10)
	for times in range(1) :
		for i in range(50) :
			er = e[i]
			print(i)
			t[i] = pool.map_async(onetime, (er,))
	
	pool.close()
	pool.join()
	plt.plot(e,t,'r-*')
	plt.show()