import os
from db_model import Base
from db_conn


def init_db():
    db_path = os.getenv("DATABASE_URL", "")
