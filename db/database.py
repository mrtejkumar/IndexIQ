# db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DB_PATH

# Define base for models
Base = declarative_base()

# Create engine
engine = create_engine(DB_PATH, echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency to use in modules
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database schema
def init_db():
    from db import models
    Base.metadata.create_all(bind=engine)
