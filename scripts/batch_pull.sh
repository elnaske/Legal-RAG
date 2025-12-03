#!/bin/bash
#SBATCH -J pull-data                  # Job name
#SBATCH --partition=general           # Partition name (use "general" or appropriate partition)
#SBATCH -o data_pull%j.txt            # Standard output file with job ID
#SBATCH -e data_pull%j.err            # Standard error file with job ID
#SBATCH --mail-type=ALL               # Email notifications for all job events
#SBATCH --mail-user=<enter-email>     # Email address for notifications
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --ntasks-per-node=1           # Number of tasks per node
#SBATCH --cpus-per-task=4
#SBATCH --time=2-00:00:00             # Requested time for process to run
#SBATCH --mem=64gb                    # Memory allocation (250 GB)
#SBATCH -A <number>                   # SLURM account name

# example path
cd /N/project/ <path-to-LRAG >/Legal-RAG || return

# pull 1000 pages of results
bash scripts/pull_data.sh 1000
