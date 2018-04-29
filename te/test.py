import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.rcParams['font.family'] = 'simhei'
mpl.rcParams['axes.unicode_minus'] = False


plt.plot(range(10),range(10),label="测试")
plt.plot(range(5),range(5),label="测试2")
plt.legend()
plt.show()