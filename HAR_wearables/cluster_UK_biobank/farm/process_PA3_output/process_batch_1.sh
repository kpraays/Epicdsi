#! /bin/bash
# ====================================
#SBATCH --job-name=process_proportions
#SBATCH --cpus-per-task=8
#SBATCH --mem=20GB
#SBATCH --time=0-02:59
#SBATCH --output=job_logs/process_proportions_%j.out
#SBATCH --mail-user=
#SBATCH --mail-type=ALL
#SBATCH  --account=
# ====================================
module load python/3.10 scipy-stack
cd /process_PA3_output

python /process_PA3_output/convert.py /processed_minute/batch_1 /process_PA3_output/assigned_labels/batch_1 /process_PA3_output/proportions_one_minute/batch_1
