from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from te import TE

data = pd.read_csv("data/dataset.csv")
data = data.values

m,n = data.shape

a = TE(data[:,1],data[:,2])
n = range(2,50)
mi1 = list(range(2,50))
mi2 = list(range(2,50))
for i in range(2,50) :
	print(i)
	mi1[i-2] = a.kde_te12(r=i, out_length=10)
	mi2[i-2] = a.kde_te21(r=i, out_length=10)

plt.plot(n,mi2,'-o',n,mi1,'-*')
#plt.plot(data[:,0],data[:,1],data[:,0],data[:,2])
plt.show()

#方向21竟然完美的保持为0，我觉得有点不可思议，应该是因为代码中的自动处理产生的结果