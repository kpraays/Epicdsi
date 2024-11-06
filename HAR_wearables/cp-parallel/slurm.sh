#! /bin/bash
# ====================================
#SBATCH --job-name=process_single_direc
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
#SBATCH --time=0-00:29
#SBATCH --output=./slurm_output/direc_%j.out
#SBATCH --mail-user=
#SBATCH --mail-type=ALL
#SBATCH --account=
# ====================================

# if [$# -eq 0]; then
#     echo "Usage: $0 <input_argument>"
#     exit 1
# fi

# input_arg=$1

source /.csvkit/bin/activate
cd /cp-parallel

# Launch python job
# (time python cp_calculate.py "UKBioBank data" "$input_arg" "/cp-parallel/outputs") 2>&1 | tee -a /cp-parallel/logs/"$input_arg".txt

(time python cp_calculate.py "UKBioBank data" 11 "/cp-parallel/outputs") 2>&1 | tee -a /cp-parallel/logs/11.txt
