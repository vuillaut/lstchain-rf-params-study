#!/bin/sh

### 1 step : choice material (gpu , node , cpu , task )
#SBATCH --job-name={JOB_NAME}

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16GB


### 3 step : create file output and error
#SBATCH --output=jobs/{JOB_NAME}.output
#SBATCH --error=jobs/{JOB_NAME}.error

### 4 step : receive information about job
#SBATCH --mail-user=thomas.vuillaume@cta-consortium.org
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END

### 5 step : options


########  load environment conda ##########################################################
source /fefs/home/thomas.vuillaume/.bashrc
conda activate lstMCpipe