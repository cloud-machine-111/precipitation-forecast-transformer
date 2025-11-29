#!/bin/bash
#SBATCH --job-name=era5
#SBATCH --partition=batch
#SBATCH --output=era5_%j.out
#SBATCH --error=era5_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=7-00:00:00   # not enforced but good practice

echo "Starting job on: $(hostname)"
echo "Time: $(date)"

# Load modules if your cluster requires them
module load python/3.10.12

# Activate your conda environment
source ~/.bashrc
conda activate res

# Run your script
python3 download_era5_amazon.py

echo "Job finished at: $(date)"
