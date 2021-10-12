i#!/usr/bin/python3

import os
from numpy import *
import copy
import sys
import itertools
from pathlib import Path


class Atom:
    def __init__(self,x,y,z,name,element):
        self.name = name
        self.element = element
        self.x = array([x,y,z])

system = []
system.append(Atom(-3,0,0,"He","He"))
system.append(Atom(0,3,0,"He","He"))
system.append(Atom(0,-3,0,"He","He"))
system.append(Atom(0,0,3,"He","He"))
system.append(Atom(0,0,-3,"He","He"))
system.append(Atom(0,0,0,"He","He"))
system.append(Atom(12345,0,0,"He","He"))


for size in range(1,len(system)):
    for i, combination in enumerate(itertools.combinations(range(len(system)),size)):
        name = str(size) + "/" + str(i)
        Path("outputFiles/{}".format(name)).mkdir(parents=True, exist_ok=True)
        fileName = "outputFiles/{}/input.inp".format(name)
        with open(fileName, "w") as f:
            f.write("! CCSD(T) verytightscf aug-cc-pvtz NoAutoStart\n\n")
            f.write("%mdci\n")
            f.write("MaxIter 100\n")
            f.write("STol 1e-6\n")
            f.write("end\n\n")
            f.write("%pal\n")
            f.write("nprocs {}\n".format(size))
            f.write("end\n\n")
            f.write("%MaxCore 5000\n")
            f.write("\n\n")
            f.write("*xyz 0 1\n")
            for j, atom in enumerate(system):
                if j in combination:
                    f.write("{} {} {} {}\n".format(system[j].element,system[j].x[0],system[j].x[1],system[j].x[2]))
                else:
                    f.write("{} : {} {} {}\n".format(system[j].element,system[j].x[0],system[j].x[1],system[j].x[2]))
            f.write("*\n")
            f.write("$new_job")
            f.write("\n")
            f.write("! CCSD(T) verytightscf aug-cc-pvqz NoAutoStart\n\n")
            f.write("%mdci\n")
            f.write("MaxIter 100\n")
            f.write("STol 1e-6\n")
            f.write("end\n\n")
            f.write("%pal\n")
            f.write("nprocs {}\n".format(size))
            f.write("end\n\n")
            f.write("%MaxCore 5000\n")
            f.write("\n\n")
            f.write("*xyz 0 1\n")
            for j, atom in enumerate(system):
                if j in combination:
                    f.write("{} {} {} {}\n".format(system[j].element,system[j].x[0],system[j].x[1],system[j].x[2]))
                else:
                    f.write("{} : {} {} {}\n".format(system[j].element,system[j].x[0],system[j].x[1],system[j].x[2]))
            f.write("*\n")


