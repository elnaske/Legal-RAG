"""
File to initialize SQL database on machine.
"""

import os
from pathlib import Path

# from src.vectorstore.db_model import Base
from .db_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# to get repo root for creating SQL metadata
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "SQL"

# Getting the db file (on slate)
DB_PATH = SQL_DIR / "metadata.db"
# need to reset on slate
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# building DB connection
db_connection = create_engine(
    DATABASE_URL,
    future=True,
    # to allow acces from different threads
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)

# create session object to use this db connection
SessionLocal = sessionmaker(bind=db_connection, autoflush=False)


# NOTE: NEED TO PASS DATABASE_URL
# one time initialization
def init_db():
    print(f"Creating tables for SQLite db: {DATABASE_URL}")
    Base.metadata.create_all(bind=db_connection)
    print("Setup of DB complete")


if __name__ == "__main__":
    init_db()
