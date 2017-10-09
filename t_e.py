import numpy as np
from matplotlib import pyplot as plt
from random import random
from math import log2,log

Nxn1xnyn = {'000':0,'001':0,'010':0,'011':0,'100':0,'101':0,'110':0,'111':0}
Nxn = {'0':0,'1':0}
Nxnyn = {'00':0,'01':0,'10':0,'11':0}
Nxn1xn = {'00':0,'01':0,'10':0,'11':0}

def func(x) :
	if x<0.5 :
		return 2*x
	else :
		return 2-2*x

def onetime(x,y,e,signal) :
	xn1 = func(e*y+(1-e)*x)
	cxn1,cx,cy='0','0','0'
	if xn1 >= 0.5 :
		cxn1 = '1'

	if x >= 0.5 :
		cx = '1'

	if y >= 0.5 :
		cy = '1'
	if signal :
		global Nxn1xn
		global Nxn
		global Nxnyn
		global Nxn1xnyn
		Nxn1xnyn[cxn1+cx+cy] += 1
		Nxn[cx] += 1
		Nxnyn[cx+cy] += 1
		Nxn1xn[cxn1+cx] += 1

	return xn1

def iterate(times,e) :

	record_after = 0

	x0 = random()
	for i in range(times) :
		y = random()
		
		x0 = onetime(x0, y, e,i>record_after)


	res = 0

	for i in ('0','1') :
		for j in ('0','1') :
			for k in ('0','1') :

				if not Nxnyn[j+k]*Nxn1xn[i+j] == 0 :
					res += Nxn1xnyn[i+j+k]*log((Nxn1xnyn[i+j+k]*Nxn[j])/(Nxnyn[j+k]*Nxn1xn[i+j]))

	return res/(times-record_after)

if __name__ == '__main__' :
	e = list(range(10))
	t = list(range(10))
	for i in range(10) :
		t[i] = iterate(200000,0.005*e[i])
		e[i] = 0.005*e[i]
	plt.plot(e,t,'r-*')
	plt.show()



