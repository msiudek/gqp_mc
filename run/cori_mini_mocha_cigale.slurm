#!/bin/bash
#SBATCH --qos=regular
#SBATCH --time=00:30:00
#SBATCH --constraint=haswell
#SBATCH -N 1
#SBATCH -J cigale_legacy
#SBATCH -o _cigale_legacy.o
#SBATCH -L SCRATCH,project

now=$(date +"%T")
echo "start time ... $now"

module load python

source activate gqp
source ~/.bashrc.ext 

export HDF5_USE_FILE_LOCKING=FALSE

n_cpu=32


######################################################
# photometry
######################################################
echo 'fitting photometry of galaxies #' 
# no noise
#noise='none'
# yes noise 
noise='legacy'
srun -n 1 -c $n_cpu python /global/homes/m/msiudek/mock_challenge/gqp_mc/run/cigale_mini_mocha.py mini_mocha $noise $n_cpu True True True False True True True
now=$(date +"%T")
echo "end time ... $now"
