#!/bin/bash
#SBATCH --job-name=pyquopt
#SBATCH --account=ANLQAT
##SBATCH --partition=bdwall
#SBATCH --partition=bdws
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --output=quopt.out
#SBATCH --error=quopt.error
#SBATCH --mail-user=mbowman@anl.gov # Optional if you require email
#SBATCH --mail-type=ALL # Optional if you require email
#SBATCH --time=01:00:00
# Set up Environment
# [Blank] -- conda environment persists

# Test
echo -e "Slurm job ID: $SLURM_JOBID"
# cd $PBS_O_WORKDIR
cd $SLURM_SUBMIT_DIR
# A little useful information for the log file...
echo -e "Master process running on: $HOSTNAME"
# echo -e "Directory is:  $PWD"
# Put in a timestamp
echo Starting execution at: `date`
cd ..
cmd="srun mpiexec -n 16 python /home/mbowman/Toffoli-Optimization/applications/context/linear_toffoli.py"
echo The command is: $cmd
echo End PBS script information.
echo ==========================================================
# echo -e "All further output is from the process being run and not the pbs script.\n$cmd\n\n"
export OMP_NUM_THREADS=10
# ls
pwd
$cmd
# Print the date again -- when finished
echo ==========================================================
echo Finished at: `date`
