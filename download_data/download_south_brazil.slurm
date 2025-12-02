#!/bin/bash
#SBATCH --job-name=era5_south_brazil
#SBATCH --output=/users/hsoaresb/data/hsoaresb/era5_south_brazil_%j.out
#SBATCH --error=/users/hsoaresb/data/hsoaresb/era5_south_brazil_%j.err
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=7-00:00:00

echo "SLURM job started on: $(date)"

# Activate your conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate res

# Move to directory where script is located
cd $SLURM_SUBMIT_DIR

echo "Running Python download script..."
python3 download_era5_south_brazil.py

echo "SLURM job finished on: $(date)"