#!/bin/bash

#BSUB -J test[1-6]
#BSUB -n 8
#BSUB -R "select[avx2] span[hosts=1]"
#BSUB -W 4:00
#BSUB -o stdout.%J
#BSUB -e stderr.%J

. /usr/share/Modules/init/bash
module purge
module load openmpi/3.1.3/2019

cd $LSB_JOBINDEX

for i in `find . -maxdepth 1 -mindepth 1 -type d -printf '%f\n'`
do
cd $i
/gpfs_common/share01/ssp/mkmostro/orca_4_2_1_linux_x86-64_openmpi314/orca input.inp > runlog.log
cd ..
done

cd ..
