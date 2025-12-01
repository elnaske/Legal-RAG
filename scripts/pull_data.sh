#!/usr/bin/bash

set -euo pipefail

# Setting up Relational DB if none exists
# DB directory
SQL_DB=$(
	python3 - <<'EOF'
from src.utils import load_config
print(load_config()["sql_db"]["root_dir"])
EOF
)

# making sure directory exists, else creating one
if [ -d "$SQL_DB" ]; then
	echo "SQL_DB directory exists at '$SQL_DB' "
else
	echo "SQL db directory doesn't exist..."
	mkdir -p "./SQL"
	echo "SQL db directory created at '$SQL_DB'"
fi

# Pulling data
echo -e "\nPulling data...\n"
uv run -m src.bin.pull_data

# Download spaCy model for preprocessing
uv run -m spacy download en_core_web_sm

# Preprocessing / Adding to vector DB
echo -e "\nPreprocessing documents and uploading them to the vector database...\n"
uv run -m src.bin.setup_vecdb
