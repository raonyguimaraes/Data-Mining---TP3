#!/bin/bash -x

#SBATCH --job-name="DM_analysis"
###SBATCH --ntasks 8
####SBATCH --nodes 1
#SBATCH --partition long
#SBATCH --mail-type=ALL
#SBATCH --mail-user=raonyguimaraes@gmail.com

#$SLURM_JOB_ID
##################### DEFINE VARIABLES ###############################

EMAIL=raonyguimaraes@gmail.com

python2.6 parse.py > tmp
