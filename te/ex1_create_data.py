import numpy as np
from copy import deepcopy
import os

def f(a,b,e) :
	c = e*a+(1-e)*b
	#print(c)
	r = deepcopy(c)
	c = c*2*(c<0.5) + (2-2*c)*(c>=0.5)
	#c[r<0.5] = 2*c[r<0.5]
	#c[r>=0.5] = 2-2*c[r>=0.5]

	return c

def f1(a,b,e) :
	c = e*a + (1-e)*b

	c = 2*c if c<0.5 else 2-2*c

	return c


def init(times,e) :
	record = np.zeros([100,2], dtype=np.float64)
	record[:,0] = np.random.random([100,1]).flatten()

	for i in range(times) :
		record[0,(i+1)%2] = f(record[-1,i%2], record[0,i%2],e)
		record[1:,(i+1)%2] = f(record[:-1,i%2], record[1:,i%2],e)

	return record[:,(i+1)%2]

def generate(init_times,record_times,e,filename,save="last") :
	origin = init(init_times, e)

	record = np.zeros([100,record_times], dtype=np.float64)
	record[:,0] = origin

	for i in range(1,record_times) :
		record[0,i] = f(record[-1,i-1], record[0,i-1],e)
		record[1:,i] = f(record[:-1,i-1], record[1:,i-1],e)
	if save=="last" :
		last_two = record[-2:,:]
	elif save=="first" :
		last_two = record[:2,:]
	last_two = last_two.transpose()
	#print(last_two.shape)

	if '.' in filename :
		filename = filename[:filename.index('.')]
	with open(filename+".csv",'wb') as fi :
		for i in range(record_times) :
			fi.write(bytes("%.3f, %.3f"%(last_two[i,0],last_two[i,1]),'utf-8'))
			if not i==record_times-1 :
				fi.write(b'\n')

if __name__ == "__main__" :
	try :
		os.mkdir("data/data1")
	except :
		pass
	e = np.array(range(26),dtype=np.float32)
	e = e*0.002
	for j in range(10) :
		for i in range(26) :
			generate(100000, 100000, e[i], 'data/data1_first_two/'+str(j)+"_"+str(i)+".csv",save="first")


