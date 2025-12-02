#!/bin/bash
#SBATCH --job-name=era5_chirps
#SBATCH --output=era5_chirps_%j.log
#SBATCH --time=14-00:00:00
#SBATCH --ntasks=1
#SBATCH --partition=batch

module purge
source /users/hsoaresb/miniconda3/etc/profile.d/conda.sh
conda activate eeps1400.venv

python download_chirps.py
