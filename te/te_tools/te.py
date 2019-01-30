import numpy as np
from time import time
from .box_kde import te_box_kde, mi_box_kde
#from numpy import sum, abs, max, zeros, log2, min
#据称和验证，停止使用属性访问方式可以，对于大规模的循环，可以提升几个百分点的性能

__all__ = ["TE",]
np.set_printoptions(threshold=np.nan)

class TE :
	def __init__(self, series1, series2) :
		self.s1 = series1
		self.s2 = series2
		self.l = len(self.s1)
		self.out = True


	#起初是考虑到便捷，将一些方法做了不太必要的封装，之后为了保持一致性，就都封装了一下，其实没必要
	def mi(self, method="discrete", out_length=0, num=20, r=0, core_language="c") :
		if method == "discrete" :
			return self.MI_Discrete(self.s1, self.s2, num)
		elif method == "box_kde" :
			if core_language == "c" :
				return self.MI_Box_KDE_C(self.s1, self.s2, r, out_length)
			elif core_language == "python" :
				return self.MI_Box_KDE(self.s1, self.s2, r, out_length)

	def te(self, method="discrete", direction="1->2", num=20, r=0, out_length=0, core_language = "c", correction=False) :
		if method == "discrete" :
			if direction == "1->2" :
				return self.TE_Discrete(self.s1, self.s2, num)
			elif direction == "2->1" :
				return self.TE_Discrete(self.s2, self.s1, num)
		elif method == "box_kde" :
			if direction == "1->2" :
				if core_language == "c" :
					return self.TE_Box_KDE_C(self.s1, self.s2, r, out_length)
				elif core_language == "python" :
					return self.TE_Box_KDE(self.s1, self.s2, r, correction, out_length)
			elif direction == "2->1" :
				if core_language == "c" :
					return self.TE_Box_KDE_C(self.s2, self.s1, r, out_length)
				elif core_language == "python" :
					return self.TE_Box_KDE(self.s2, self.s1, r, correction, out_length)



	def MI_Discrete(self, s1, s2, num=20) :
		'''
		利用最大似然估计计算互信息
		第一步，将原始数据按照标准进行离散化，但是我很快意识到，因为之前理解错了累加变量，我误以为需要从直方图反推
		每个点的概率，所以才加入了预先的离散化，事实上这一步并不需要，所以可以删除这一步，并且也不需要使用record
		保留上述代码，作为记录如何实现和直方图函数相匹配的离散化
		'''

		'''
		record = np.zeros([self.l, 5], dtype=np.int64)
		s = s1[:] - np.min(s1[:])
		s /= (np.max(s)/num)
		s = s.astype(np.int32)
		s[np.where(s==num)] = num-1
		record[:, 0] = s
		'''

		hist_x = np.histogram(s1, bins=num)[0]  
		#对序列1进行直方图统计，只需要返回结果的第一个
		hist_y = np.histogram(s2, bins=num)[0]  
		#对序列2进行直方图统计，只需要返回结果的第一个
		hist_xy = np.histogram2d(s1, s2, bins=num)[0]   
		#对序列1和2进行二维直方图统计，只需要返回结果的第一个

		hist_x = hist_x.reshape(num,1)   
		#需要使用序列1和2的统计结果相乘生成p(x)*p(y)，为借助广播原则的便捷，我们需要reshape
		hist_y = hist_y.reshape(1,num)

		hist_x_y = hist_x*hist_y

		hist_x_y = hist_x_y[hist_xy>0]  
		#从所有结果中筛除p(x,y)为0的结果，相当于去掉二维格子中没有点的格子，因为逻辑运算的特点，结果将是被展开为1维
		hist_xy = hist_xy[hist_xy>0]

		return np.sum(hist_xy*np.log2(hist_xy*self.l/hist_x_y))/self.l     
		#按照公式进行计算，注意之前得到的都是点数，而非概率，所以经过分子分母抵消之后，分子依旧要乘上序列长度，结果为正数
		
	def MI_Box_KDE(self, s1, s2, r, out_length) :
		record = np.zeros([self.l, 2])
		record[:, 0] = s1
		record[:, 1] = s2

		p = np.zeros([self.l, 3],dtype=np.float)
		for i in range(self.l) :
			a = r-np.max(np.abs(record-record[i,:]), axis=1)
			a[np.max((0,i-out_length)):np.min((i+out_length,self.l-1))] = 0
			p[i, 0] = np.sum(a>0) #pxy
			a = r-np.abs(record[:,0]-record[i, 0])
			a[np.max((0,i-out_length)):np.min((i+out_length,self.l-1))] = 0
			p[i, 1] = np.sum(a>0) #px
			a = r-np.abs(record[:,1]-record[i,1])
			a[np.max((0,i-out_length)):np.min((i+out_length,self.l-1))] = 0
			p[i, 2] = np.sum(a>0)	#py

		p = p[p[:,0]>0, :]

		return np.sum(p[:, 0]*np.log2(p[:, 0]*self.l/(p[:, 1]*p[:, 2])))/self.l

	def MI_Box_KDE_C(self, s1, s2, r, out_length) :
		record = np.zeros([self.l, 2], dtype=np.double)
		record[:, 0] = s1
		record[:, 1] = s2

		p = np.zeros([self.l, 3],dtype=np.double)
		
		mi_box_kde(record, p, r, out_length)

		p = p[p[:,0]>0, :]

		return np.sum(p[:, 0]*np.log2(p[:, 0]*self.l/(p[:, 1]*p[:, 2])))/self.l



	def TE_Discrete(self, s1, s2, num=20) :
		'''
		首先需要按照指定的级别将原始序列离散化，然后再进行直方图统计
		同样的，预先的离散化是不必要的，只保留一个作为示例
		本方法计算从序列s1到s2的离散化传输熵
		'''
		'''
		record = np.zeros([self.l-1, 3], dtype=np.int32)
		s = s2[1:] - np.min(s2[1:])
		#print(s)
		s /= (np.max(s)/num)
		#print(s)
		s = s.astype(np.int)
		s[np.where(s==num)] = num-1
		#print(s)
		record[:, 0] = s
		'''
		record = np.zeros([self.l-1, 3], dtype=np.float)
		#因为在三维直方图统计中必须要传入一个整体，所以record变量还是有必要的
		record[:, 0] = s2[1:]
		#s2序列称为x序列，s1序列称为y序列，那么本方法就是在计算y到x的传输熵
		#从x序列中取出x(n+1)和x(n)
		record[:, 1] = s2[:-1]
		#从y序列中取出y(n)
		record[:, 2] = s1[:-1]
		#record的第0，1，2列分别是x(n+1),x(n),y(n)

		#根据公式的要求，我们需要获取x(n)，x(n+1)x(n), x(n)y(n), x(n+1)x(n)y(n)的直方图
		hist_xn = np.histogram(record[:,1], bins=num)[0]
		hist_xn1xn = np.histogram2d(record[:,0], record[:,1], bins=num)[0]
		hist_xnyn = np.histogram2d(record[:,1], record[:,2], bins=num)[0]
		hist_xn1xnyn = np.histogramdd(record[:,:3], bins=num)[0]

		#为配合广播原则，需要对相应的变量reshape
		hist_xn = hist_xn.reshape([1,num,1])
		hist_xn1xn = hist_xn1xn.reshape([num,num,1])
		hist_xnyn = hist_xnyn.reshape([1,num,num])

		#为了删除x(n+1)x(n)y(n)直方图中为0的结果，必须进行一些预先的计算，然后使用逻辑运算剔除
		h1 = hist_xn1xnyn*hist_xn
		h2 = hist_xn1xn*hist_xnyn

		h1 = h1[hist_xn1xnyn>0]
		h2 = h2[hist_xn1xnyn>0]
		hist_xn1xnyn = hist_xn1xnyn[hist_xn1xnyn>0]

		#计算，注意分子分母都应该除掉self.l的平方，刚好抵消
		return np.sum(hist_xn1xnyn*np.log2(h1/h2))/(self.l-1)

	def TE_Box_KDE(self, s1, s2, r, correction=False, out_length=100) :
		l = self.l-1
		record = np.zeros([l, 3])
		record[:, 0] = s2[1:]
		record[:, 1] = s2[:-1]
		record[:, 2] = s1[:-1]
		#print("this is record")
		#print(record)


		p_record = np.zeros([l, 4],dtype=np.float)
		if len(r)==1 :
			for i in range(l) :
				#据分析，差不多一半的时间花在了max上面，另外一半时间花在了np.ufunc.reduce
				#I don't know how to optimize, maybe Cython?
				a = r-((record-record[i,:]).__abs__()).max(axis=1)
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 0] = (a>=0).sum() #in1injn
				a = r-(record[:,1]-record[i, 1]).__abs__()
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 1] = (a>=0).sum() #in
				a = r-((record[:,1:]-record[i,1:]).__abs__()).max(axis=1)
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 2] = (a>=0).sum() #injn
				a = r-((record[:,:-1]-record[i,:-1]).__abs__()).max(axis=1)
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 3] = (a>=0).sum() #in1in
		else :
			rs1 = r[0]
			rs2 = r[1]
			for i in range(l) :
				#done! 18.5.5 10:06 检验完毕，与matlb对比一致
				#据分析，差不多一半的时间花在了max上面，另外一半时间花在了np.ufunc.reduce
				#I don't know how to optimize, maybe Cython?
				a = np.min([[rs2,rs2,rs1]]-((record-record[i,:]).__abs__()),axis=1)
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 0] = (a>=0).sum() #in1injn
				a = rs2-(record[:,1]-record[i, 1]).__abs__()
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 1] = (a>=0).sum() #in
				a = np.min([[rs2,rs1]]-((record[:,1:]-record[i,1:]).__abs__()),axis=1)
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 2] = (a>=0).sum() #injn
				a = np.min([[rs2,rs2]]-((record[:,:-1]-record[i,:-1]).__abs__()),axis=1)
				a[max(0,i-out_length+1):min(i+out_length,l)] = -1
				p_record[i, 3] = (a>=0).sum() #in1in		
		#print(p_record)
		new_p_record = p_record[p_record[:, 0]>0, :]

		#误差修正部分
		if correction :
			pass
			#巨麻烦无比，我怕是完不成了
		'''
		for i in range(l) :
			#if p_record[i, 0]>0 :
				print(i)
				print(p_record[i, :])
		'''
		#print(r)
		#print(new_p_record)
		#print("above is new_p_record")

		return (np.log2(new_p_record[:,0]*new_p_record[:,1]/(new_p_record[:,2]*new_p_record[:,3]))).sum()/(self.l-1)


	def TE_Box_KDE_C(self, s1, s2, r, out_length=100) :
		l = self.l-1
		record = np.zeros([l, 3], dtype=np.double)
		record[:, 0] = s2[1:]
		record[:, 1] = s2[:-1]
		record[:, 2] = s1[:-1]

		p_record = np.zeros([l, 4],dtype=np.double)

		te_box_kde(record, p_record, r, out_length)
		
		new_p_record = p_record[p_record[:, 0]>0, :]

		return (np.log2(new_p_record[:,0]*new_p_record[:,1]/(new_p_record[:,2]*new_p_record[:,3]))).sum()/(self.l-1)


	def TE_KDE_T(self, s1, s2, r, out_length=100) :
		'''
		一次极度失败的矢量化加速KDE尝试
		'''
		s = time()
		record = np.zeros([self.l-1, 3])
		record[:, 0] = s2[1:]
		record[:, 1] = s2[:-1]
		record[:, 2] = s1[:-1]
		p_record = np.zeros([self.l-1, 4],dtype=np.float)
		print(time()-s)
		s = time()
		a1 = record.reshape([1, self.l-1, 3])
		a5 = record.reshape([self.l-1, 1, 3])
		a1 = r-np.max(np.abs(a1-a5), axis=2)
		a5 = 0
		for i in range(-100, 101) :
			a1 *= np.logical_not(np.eye(self.l-1, k=i))
		p_record[:,0] = np.sum(a1>0, axis=1)
		a1 = 0
		print(time()-s)
		s = time()
		a2 = record[:,1].reshape([1,self.l-1])
		a5 = record[:,1].reshape([self.l-1,1])
		a2 = r-np.abs(a2-a5)
		a5 = 0
		for i in range(-100, 101) :
			a2 *= np.logical_not(np.eye(self.l-1, k=i))
		p_record[:,1] = np.sum(a2>0, axis=1)
		a2 = 0
		print(time()-s)
		s = time()
		a3 = record[:,1:].reshape([1, self.l-1, 2])
		a5 = record[:,1:].reshape([self.l-1, 1, 2])
		a3 = r-np.max(np.abs(a3-a5), axis=2)
		a5 = 0
		for i in range(-100, 101) :
			a3 *= np.logical_not(np.eye(self.l-1, k=i))
		p_record[:,2] = np.sum(a3>0, axis=1)
		a3 = 0
		print(time()-s)
		s = time()


		a4 = record[:,:-1].reshape([1, self.l-1, 2])
		a5 = record[:,:-1].reshape([self.l-1, 1, 2])
		a4 = r-np.max(np.abs(a4-a5), axis=2)
		a5 = 0
		for i in range(-100, 101) :
			a4 *= np.logical_not(np.eye(self.l-1, k=i))
		p_record[:,3] = np.sum(a3>0, axis=1)
		a4 = 0
		print(time()-s)
		s = time()
		'''

		for i in range(-100, 101) :
			a5 = np.logical_not(np.eye(self.l-1, k=i))
			a1 *= a5
			a2 *= a5
			a3 *= a5
			a4 *= a5
		p_record[:,0] = np.sum(a1>0, axis=1)
		p_record[:,1] = np.sum(a2>0, axis=1)
		p_record[:,2] = np.sum(a3>0, axis=1)
		p_record[:,3] = np.sum(a4>0, axis=1)
		'''
		p_record = p_record[p_record[:, 0]>0, :]
		return np.sum(np.log2(p_record[:,0]*p_record[:,1]/(p_record[:,2]*p_record[:,3])))/(self.l-1)



	def TE_Box_KDE_WTF(self, s1, s2, r, out_length) :
		l = self.l-1
		record = np.zeros([l, 3])
		record[:, 0] = s2[1:]
		record[:, 1] = s2[:-1]
		record[:, 2] = s1[:-1]


		'''
		numpy在进行直方图统计的时候，参数bins指定的是格子的数目，可以考虑一下，其实当我们试图做一个直方图
		统计的时候，我们可以有两种选择，指定格子数目，或者指定格子宽度，两种方式并无法直接转换，因为
		同样地格子数是有多种可能的宽度的
		那么numpy在指定格子数目的情况下，是如何实现的呢？对于一个数据序列，数据点的序号是这样得到的
		int((a-min(a))/(max(a)/bins))， 然后还必须处理a[np.where(a==bins)] = bins-1
		当我们需要一个指定格子宽度的直方图函数的时候，我们可以这样做
		首先必须计算总的格子数bins = ceil((max(a)-min(a))/width)，向上取整的意思
		然后每个点int((a-min(a))/width)， 然后还必须处理a[np.where(a==bins)] = bins-1
		'''

		hxn = np.histogram(record[:,1], bins=num)[0]



