import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_int,c_double

__all__ = ["kde_count"]


array_in = npct.ndpointer(dtype=np.double, ndim=2, flags="CONTIGUOUS")
#array_out = npct.ndpointer(dtype=np.double, ndim=1, flags="CONTIGUOUS")

libcd = npct.load_library("kde_te.dll",'.')

libcd.kde_count.restype = None
libcd.kde_count.argtypes = [array_in, array_in, c_int, c_double, c_int]

def kde_count(in_array, out_array, r, out_length) :
	return libcd.kde_count(in_array, out_array, len(in_array), r, out_length)