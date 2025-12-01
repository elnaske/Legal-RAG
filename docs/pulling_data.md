# PULLING DATA
- - - 

1. [How to pull data](#how-to-pull-data)
- - - 

### How to pull data

To pull data for both the SQL Relational Database and the Chroma database, from root, run `bash scripts/pull_data.sh`

**NOTE:** *You will want to be signed into a shared HPC for this task to download to a larger shared database if you are working on a team.* 

Running this script should create a `./SQL/` directory, where you will find relational database info pulled into `./SQL/metadata.db`. 

Running this script will also activate the vectorstore **chroma** database at `./chroma/`. 