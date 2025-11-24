#!/usr/bin/bash

set -euo pipefail

# DB directory
SQL_DB="./SQL/"

# making sure directory exists, else creating one
if [ -d "$SQL_DB" ]; then
	echo "SQL_DB directory exists at '$SQL_DB' "
else
	echo "SQL db directory doesn't exist..."
	mkdir "SQL"
	echo "SQL db directory created at '$SQL_DB'"
fi

cd src/

# run db initialization on machine
uv run -m vectorstore.SQLite_db
