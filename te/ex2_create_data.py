import numpy as np
from copy import deepcopy
import os
def f(a,b,e) :
	c = e*a+(1-e)*b
	c = 2-c**2

	return c



def init(times,e) :
	record = np.zeros([100,2], dtype=np.float64)
	record[:,0] = 4*(np.random.random([100,1]).flatten())-2

	for i in range(times) :
		record[0,(i+1)%2] = f(record[-1,i%2], record[0,i%2],e)
		record[1:,(i+1)%2] = f(record[:-1,i%2], record[1:,i%2], e)

	return record[:,(i+1)%2]

def generate(init_times,record_times,e,filename) :
	origin = init(init_times, e)

	record = np.zeros([100,record_times], dtype=np.float64)
	record[:,0] = origin

	for i in range(1,record_times) :
		record[0,i] = f(record[-1,i-1], record[0,i-1],e)
		record[1:,i] = f(record[:-1,i-1], record[1:,i-1],e)

	#last_two = record[-2:,:]
	last_two = record[:2, :]
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
		os.mkdir("data2")
	except :
		pass
	e = np.array(range(101),dtype=np.float32)
	e = e*0.01
	for i in range(101) :
		generate(100000, 10000, e[i], 'data2/'+str(i))	


