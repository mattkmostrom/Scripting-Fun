#!/bin/bash/

rm -r total_energy
rm -r energy
mkdir total_energy
mkdir energy
cd energy
rm col1
energy_dir=$(pwd)

for n in `seq 1.5 0.1 10`;do
	echo $n >> col1
done
cd ..

cwd=$(pwd)

echo ""
echo "Calculating basis set extrapolation..."
echo ""

for n in `seq 1.5 0.1 10`;do
	grep "E(0)" $n/runlog.log | grep -o [-][-.0-9]* > energies.dat
	grep "Final correlation energy" $n/runlog.log | grep -o [-][-.0-9]* >> energies.dat
	export NUMBER=`pwd | grep -o "[0-9]*$"`
python3 <<EOF
import os
import math
file_output = open("energy/temp_energy.dat", "a")
file = open("energies.dat","r")
try:
    
    X = 3
    Y = 4

    dimer_tz = float(file.readline())
    file.readline()
    mono1_tz = float(file.readline())
    file.readline()
    mono2_tz = float(file.readline())
    file.readline()
    dimer_qz = float(file.readline())
    file.readline()
    mono1_qz = float(file.readline())
    file.readline()
    mono2_qz = float(file.readline())
    file.readline()



    alpha = 5.79 		#alpha for aug-cc from ORCA depths
    #E_inf = E_x - A*Exp[-alpha*sqrt[x]]  https://www.afs.enea.it/software/orca/orca_manual_4_2_1.pdf    pg.72

    A_dimer = (dimer_tz - dimer_qz) / (math.exp(-alpha * math.sqrt(X)) - math.exp(-alpha * math.sqrt(Y)))
    HF_dimer = dimer_tz - A_dimer * math.exp(-alpha * math.sqrt(X))

    A_mono = (mono1_tz - mono1_qz) / (math.exp(-alpha * math.sqrt(X)) - math.exp(-alpha * math.sqrt(Y)))
    HF_mono1 = mono1_tz - A_mono * math.exp(-alpha * math.sqrt(X))

    HF_mono2 = HF_mono1


#    print("HF parts")
#    print(A_dimer)
#    print(A_mono)
#    print(HF_dimer)
#    print(HF_mono1)



#    beta = 3.05		#from ORCA manual
    beta = 1.585		#optimal for helium
#    beta = 2.473		#optimal for neon

    dimer_dz_corr = float(file.readline())
    mono1_dz_corr = float(file.readline())
    mono2_dz_corr = float(file.readline())
    dimer_tz_corr = float(file.readline())
    mono1_tz_corr = float(file.readline())
    mono2_tz_corr = float(file.readline())

    dimer_corr_extrap = ( X**beta * dimer_dz_corr - Y**beta * dimer_tz_corr ) / ( X**beta - Y**beta )
    mono1_corr_extrap = ( X**beta * mono1_dz_corr - Y**beta * mono1_tz_corr ) / ( X**beta - Y**beta )
    mono2_corr_extrap = ( X**beta * mono2_dz_corr - Y**beta * mono2_tz_corr ) / ( X**beta - Y**beta )

#    print("Correlation parts")
#    print(dimer_corr_extrap)
#    print(mono1_corr_extrap)
#    print("")


    file_output.write(os.environ["NUMBER"]+"\t")    
    file_output.write(str(( (HF_dimer - HF_mono1 - HF_mono2) + (dimer_corr_extrap - mono1_corr_extrap - mono2_corr_extrap))/3.166811429e-6)+"\n")

except ValueError:
    file_output.write(str(100000)+"\n")

file.close()
file_output.close()
EOF

done

cd ${energy_dir}
mv ../energies.dat .
paste col1 temp_energy.dat > energy.dat
cp energy.dat ../total_energy
cat energy.dat
cd ${cwd}
