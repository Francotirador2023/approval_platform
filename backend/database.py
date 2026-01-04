from sqlmodel import SQLModel, create_engine, Session
from models import * # Import models to register them with SQLModel

import os

sqlite_file_name = "approval.db"
# Use absolute path to ensure all scripts find the same DB
# base_dir = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(base_dir, sqlite_file_name)
db_path = r"c:\Users\jonyr\.gemini\antigravity\scratch\approval_platform\backend\approval.db"
sqlite_url = f"sqlite:///{db_path}"
# Override with env var if present (e.g. for Production)
database_url = os.getenv("DATABASE_URL", sqlite_url)

connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}
engine = create_engine(database_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
