'''
from multiprocessing import Process,Lock

#from threading import Lock

lock = Lock()
res = list(range(10))
def work(lock,k,o,res) :
	lock.acquire()
	res[o] = k
	lock.release()
p_list = []
for i in range(10) :
	p_list.append(Process(target=work,args=(lock,i+3,i,res)))

for i in p_list :
	i.start()
	#i.join()

print(res)

'''
import multiprocessing
import time

def worker(s, res, i):
    s.acquire()
    print(multiprocessing.current_process().name + "acquire");
    res[i] = i+3
    print(multiprocessing.current_process().name + "release\n");
    s.release()

if __name__ == "__main__":
    lock = multiprocessing.Lock()
    res = multiprocessing.Array('i',range(5))
    p_list = []
    for i in range(5):
        p = multiprocessing.Process(target = worker, args=(lock, res,i))
        p.start()
        p_list.append(p)
    for i in p_list :
    	i.join()
    print(res[:])