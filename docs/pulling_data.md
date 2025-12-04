# PULLING DATA
- - - 

1. [How to pull data](#how-to-pull-data)
2. [Sbatching for HPC](#how-to-submit-a-data-pull-on-an-hpc-as-a-batch-job)
- - - 

### How to pull data

**Note:** *You will want to be signed into a shared HPC for this task to download to a larger shared database if you are working on a team.* 

To pull data for both the SQL Relational Database and the Chroma database, from root, run `bash scripts/pull_data.sh`

##### Defining how much data you want to pull

One of the things that's a limitation to using CourtRuler's REST API is that if you don't do something to keep iterating through response pages, it'll stop after the first result. To work around this, we've set up some controllable iteration to continue to pull data from subsequent pages. 

**Note:** *if you don't add an integer value and call it without an appended number, it'll default to one page*

To do this, from the root, run the same script `bash scripts/pull_data`, just just append an integer value to the end.  Example: 

```bash
# we want to pull six REST API result pages of data
bash scripts/pull_data.sh 6
```
Some of the console output we should see will look like the following:
```bash
SQL_DB directory exists at './SQL/'

Pulling data (max pages: 6)...

Creating tables for SQLite db: sqlite:////<your-path>/Legal-RAG/SQL/metadata.db
Setup of DB complete
Total Results: 1532092

********************
Pulling Page #1 of 6
********************
--------------------
10673681 PIZARRO (KARLO) v. STATE (CRIMINAL)
https://www.courtlistener.com/api/rest/v4/opinions/11140268/
--------------------
```


As you can see, running this script should create a `./SQL/` directory, where you will find relational database info pulled into `./SQL/metadata.db`. 

Running this script will also activate the vectorstore **chroma** database at `./chroma/`. 

Let this process run until you've gotten confirmation that the opinions have been stored in the vector database.

- - - 

### How to submit a data pull on an HPC as a batch job

If you want to submit a batch job to run on an HPC, where it will continue to run if you end the `ssh`connection, use `sbatch`.

To define this, you'll want to create another `.sh` script like the following example as a template (this is not an exhaustive list of args):

```bash
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
cd /N/project/<path-to-LRAG>/Legal-RAG || return

# pull 1000 pages of results
bash scripts/pull_data.sh 1000

```
Then from the command line at root, run `sbatch scripts/batch_pull.sh`
- - - 