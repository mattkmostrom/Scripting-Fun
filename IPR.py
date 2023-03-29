import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os
import numpy as np
import math

eigvect = np.loadtxt('eigvects.dat')
eigval = np.loadtxt('eigvals.dat')
natoms = eigvect.shape[0] // 3

#f = open("eigvect_tpose.dat", "w")
#f.write(str(np.transpose(eigvect)) + "\n")
#f.close()

#f = open("eigval_tpose.dat", "w")
#f.write(str(np.transpose(eigval)) + "\n")
#f.close()

print('Atom count:',natoms)

#   /x1 x2 x3    \
#   |y1 y2 y3 ...|  
#   |z1 z2 z3    |     eigenvectors are columns, not rows
#   |    .       |
#   |    .       |
#   \    .       /

# num = sum Dij ** 4
num = eigvect**4
num = np.sum(num, axis=0)

# denom = (sum Dij ** 2) ** 2
denom = eigvect**2
denom = np.sum(denom, axis=0)
denom = denom**2

IPR = num / denom

print("\n\n------------------------------------\n","Eigvals, IPRs: \n")
for i in range(len(eigval)):
    print(eigval[i],IPR[i])

print("Xe frequency^2: 0.27139")

f = open("IPR.dat", "w")
f.write(str(IPR) + "\n")
f.close()
