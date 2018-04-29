import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from te import TE
import matplotlib as mpl
import time
import multiprocessing as mp



def work(o) :
	print(o,'begin')
	data = pd.read_csv("data/data2/"+str(o)+'.csv', names=['s1','s2'])
	data = data.values
	a = TE(data[:,0], data[:,1])

	return o,a.kde_te12(r=0.3),a.kde_te21(r=0.3)
	
if __name__ == '__main__':
	start = time.time()
	mpl.rcParams['font.family'] = 'simhei'
	mpl.rcParams['axes.unicode_minus'] = False
	res = np.zeros([2,101])

	all_work = []
	pool = mp.Pool(4)

	for i in range(101) :
		all_work.append(pool.apply_async(func=work,args=(i,)))
	pool.close()
	pool.join()

	for i in all_work :
		order, te1, te2 = i.get(timeout=10)
		res[0,order] = te1
		res[1,order] = te2



	e = np.array(range(101), dtype=np.float)
	e = e*0.01

	print(time.time()-start)
	ex2 = np.loadtxt("SchreiberExample2.txt")
	plt.plot(e,res[0,:],'-*',label="模拟值")
	plt.plot(e,res[1,:],'-*',label="模拟值")
	plt.plot( ex2[:,0], ex2[:,1], 'r-o', label="论文中的计算值")
	plt.legend()
	plt.xlabel("耦合系数")
	plt.ylabel("传输熵")
	plt.title("原始论文例2模拟效果对比")
	plt.show()
