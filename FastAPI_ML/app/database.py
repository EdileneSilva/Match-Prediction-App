import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_ML_URL = os.getenv(
    "DATABASE_ML_URL",
    "postgresql://postgres:postgres@localhost:5432/footballprediction_db"
)

engine = create_engine(DATABASE_ML_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency FastAPI — session vers footballprediction_db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
