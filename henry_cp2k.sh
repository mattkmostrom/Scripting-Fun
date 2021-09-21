#!/bin/bash
#BSUB -n 20
#BSUB -R "select[avx2] span[hosts=1]"
#BSUB -W 1:00
#BSUB -J cp2k
#BSUB -o stdout.%J
#BSUB -e stderr.%J

. /usr/share/Modules/init/bash
module purge
module load cmake intel intel_mpi mkl conda
source /usr/local/usrapps/ssp/cp2k-8.1.0/tools/toolchain/install/setup
export PATH=$PATH:/usr/local/usrapps/ssp/cp2k-8.1.0/exe/local
export CP2K_DATA_DIR=/usr/local/usrapps/ssp/cp2k-8.1.0/data

export OMP_NUM_THREADS=1

mpirun cp2k.psmp -i *.inp -o runlog.log
