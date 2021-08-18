#!~/bin/bash

rm configuration_energies.dat
touch configuration_energies.dat

for n in $(seq 1.75 0.25 6.00);do
	
	cd $n
  echo ""
	echo $n
  cd outputFiles
  echo $n >> ../../configuration_energies.dat
  for m in `ls -d */`; do 
    
    cd $m
    for tuple in `ls -d */`;do
      cd $tuple
      pwd
      grep "E(0)" runlog.log | grep -o "[-][-.0-9]*" > energies.dat
	    grep "Final correlation energy" runlog.log | grep -o "[-][-.0-9]*" >> energies.dat

python3 <<END
import os
import math
import numpy
file_output = open("../../../../configuration_energies.dat", "a")
file = open("energies.dat","r")
cwd = os.getcwd()
try:

    dir = cwd.split('/')
    ID = dir[len(dir)-2]
    print(ID)

    data = numpy.zeros(3)

    tz_hf = float(file.readline())
    file.readline()
    qz_hf = float(file.readline())
    file.readline()

    tz_corr = float(file.readline())
    qz_corr = float(file.readline())
    

    for i in range(len(data)):
      data[0] = qz_corr
      data[1] = tz_corr
      data[2] = qz_hf
    
    line = str(ID) + " " + str(data[0]) + " " + str(data[1]) + " " + str(data[2]) + "\n"
    file_output.write(line)



except ValueError:
    file_output.write(str(100000)+"\n")
file.close()
file_output.close()
import pprint
pp = pprint.PrettyPrinter(indent =4)
pp.pprint(data)
#for item in data:
#  print(f"{item},",end='')
END
      cd ..
    done #tuple
    cd ..
  done #m
	
  cd ../..

done #n

