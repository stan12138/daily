import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_int,c_double
import os

__all__ = ["te_box_kde", "mi_box_kde"]


array_in = npct.ndpointer(dtype=np.double, ndim=2, flags="CONTIGUOUS")
#array_out = npct.ndpointer(dtype=np.double, ndim=1, flags="CONTIGUOUS")

libcd = npct.load_library("box_kde.dll",os.path.dirname(__file__))

libcd.te_box_kde.restype = None
libcd.te_box_kde.argtypes = [array_in, array_in, c_int, c_double, c_int]

libcd.mi_box_kde.restype = None
libcd.mi_box_kde.argtypes = [array_in, array_in, c_int, c_double, c_int]

def te_box_kde(in_array, out_array, r, out_length) :
	return libcd.te_box_kde(in_array, out_array, len(in_array), r, out_length)

def mi_box_kde(in_array, out_array, r, out_length) :
	return libcd.mi_box_kde(in_array, out_array, len(in_array), r, out_length)