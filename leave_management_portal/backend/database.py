"""
database.py
------------
Sets up the SQLite database engine, the session factory, and the
declarative Base that every model inherits from.

Nothing fancy here on purpose -- one file, one job.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file lives next to this file inside backend/
DATABASE_URL = "sqlite:///./leave_management.db"

# check_same_thread=False is required for SQLite when used with FastAPI,
# since FastAPI can hand requests to different threads.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
