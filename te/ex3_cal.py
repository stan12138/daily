import numpy as np
import matplotlib.pyplot as plt
from te_tools.te import TE
import matplotlib as mpl
import time

start = time.time()
mpl.rcParams['font.family'] = 'simhei'
mpl.rcParams['axes.unicode_minus'] = False

rs = [0.01, 0.016, 0.023, 0.032, 0.047, 0.064, 0.09, 0.12, 0.18, 0.26, 0.36, 0.50, 0.65, 1.0]
#rs = [0.01]
#data = np.loadtxt("data/test_data.txt")
data = np.loadtxt("data/heart1.txt")
#data = np.loadtxt("data/heart_50.txt")
#data = np.loadtxt("data/heart.csv")
heart = data[:,0]
chest = data[:,1]
l = len(heart)

h1 = heart[:-1]
c1 = chest[:-1]
std_h = np.sqrt(np.sum((h1-np.sum(h1)/(l-1))**2)/(l-2))
std_c = np.sqrt(np.sum((c1-np.sum(c1)/(l-1))**2)/(l-2))
#heart = heart-np.sum(heart)/l
#heart *= l/np.sqrt(np.sum(heart*heart))

#chest -= np.sum(chest)/l
#chest *= l/np.sqrt(np.sum(chest*chest))

l = len(rs)

res1 = list(range(l))
res2 = list(range(l))

for i in range(l) :
	#print("\r", i, end="")
	r = rs[i]
	rh = r*std_h
	rc = r*std_c
	a = TE(heart, chest)
	b = TE(chest, heart)
	res1[i] = a.te(method="box_kde", direction="1->2", r=(rh,rc), out_length=100, core_language="python")
	res2[i] = b.te(method="box_kde", direction="1->2", r=(rc,rh), out_length=100, core_language="python")
	print("TE(r=%f): heart->breath = %f, breath->heart = %f"%(rs[i], res1[i], res2[i]))
print("\n")
print(time.time()-start)
fig = plt.figure()
ax = fig.add_subplot(111)
line1 = ax.plot(rs, res1, "-*")
line2 = ax.plot(rs, res2, "-o")
ax.set_xscale("log")

plt.show()
