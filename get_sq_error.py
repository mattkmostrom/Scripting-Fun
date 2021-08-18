#!/usr/bin/python
# -*- coding: utf-8 -*-

# Calculate the sq_error, AKA the residual sum of squares (RSS)

import numpy as np
import scitools.filetable as ft
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
	xmgrace = sys.argv[1]
    else:
	print "Usage: $python get_sq_error.py [sigma.xmgrace.dat]"
	sys.exit(1)

    with open("/home/ccioce/He/HeHe.dat") as predicted:
        r1, en1 = ft.read_columns(predicted)

    with open(xmgrace) as observed:
        r2, en2 = ft.read_columns(observed)

    # First, prune any values that are greater than 100 K, as this is our max_energy threshold for surface fits
    en3 = []
    for item in en2:
        if item < 100.0:
    	    en3.append(item)
    
    # Now, remove as many items from the CCSD(T) energy list
    en4 = en1.tolist()
    en4.reverse()
    diff = 120.0 - len(en3)
    for j in range(int(diff)+1):
        en4.pop()
    en4.reverse()
    
    # Finally, get the residual and then the sum of the squares
    en3 = np.array(en3)		# This is OBSERVED  (i.e. classical)
    en4 = np.array(en4)		# This is PREDICTED (i.e. ab initio)
    residual = en3 - en4
    #for item in residual:
    #    print "%.6f" % item
    
    print(np.sum(np.square(residual)))

