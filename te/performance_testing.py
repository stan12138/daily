import cProfile
import pandas as pd
import numpy as np

from te import TE

import time

def work(o) :
	print(o,'begin')
	data = pd.read_csv("data/data2/"+str(o)+'.csv', names=['s1','s2'])
	data = data.values
	a = TE(data[:,0], data[:,1])

	return o,a.kde_te12(r=0.3),a.kde_te21(r=0.3)

prof = cProfile.Profile()
prof.enable()

work(10)

prof.create_stats()
prof.print_stats()