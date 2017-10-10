import numpy as np
from matplotlib import pyplot as plt
from random import uniform
from math import log2,log
from copy import deepcopy
import time

def func(x) :
	return 2-x**2


def iterate(times,e) :
	record = np.zeros([10000,3], dtype=np.float64)
	record_after = 100000
	x = uniform(-2, 2)
	y = uniform(-2, 2)
	for i in range(110000) :
		x1 = func(e*y+(1-e)*x)
		if i>=100000 :
			record[i-100000,0] = x1
			record[i-100000,1] = x
			record[i-100000,2] = y
		x = x1
		y = uniform(-2, 2)
	return record
def ke(record,r) :
	m= record.shape[0]
	if len(record.shape) == 1 :
		record.shape = (m,1)
	p = np.arange(m, dtype=np.float64)
	p = p.flatten()
	for i in range(m) :
		a = record[i,:]
		p[i] = sum(r-np.sqrt(np.sum((a-record)**2,axis=1)))
	p = p/np.sum(p)
	p = p/m
	return p


if __name__ == '__main__' :
	e = list(range(10))
	t = list(range(10))
	r = 0.2
	for i in range(10) :
		now = time.time()
		record = iterate(0,0.01*e[i])
		
		print("generate done , use %s seconds"%(time.time() - now))
		now = time.time()
		Nxn1xnyn = deepcopy(record)
		Nxn = deepcopy(record[:,1])
		Nxnyn = deepcopy(record[:,(1,2)])
		Nxn1xn = deepcopy(record[:,(0,1)])
		
		print("copy done , use %s seconds"%(time.time() - now))
		now = time.time()

		pxn1xnyn = ke(Nxn1xnyn, r)

		print("first kernel estimation done , use %s seconds"%(time.time() - now))
		now = time.time()
		pxn = ke(Nxn, r)
		print("second kernel estimation done , use %s seconds"%(time.time() - now))
		now = time.time()
		pxnyn = ke(Nxnyn, r)
		print("third kernel estimation done , use %s seconds"%(time.time() - now))
		now = time.time()
		pxn1xn = ke(Nxn1xn, r)
		print("fourth kernel estimation done , use %s seconds"%(time.time() - now))
		now = time.time()
		t[i] = sum(pxn1xnyn*np.log2((pxn1xnyn*pxn)/(pxnyn*pxn1xn)))
		e[i] = 0.01*e[i]
		print("%s is done!"%i)
	plt.plot(e,t,'r-*')
	plt.show()