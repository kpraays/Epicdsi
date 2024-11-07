#!/bin/bash
# Here you should provide the sbatch arguments to be used in all jobs in this serial farm
# It has to contain the runtime switch (either -t or --time):
#SBATCH --time=1:0:0
#SBATCH --mem=12G
#  You have to replace Your_account_name below with the name of your account:
#SBATCH --account=

# Don't change this line:
task.run
