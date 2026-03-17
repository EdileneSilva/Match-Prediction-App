import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_APP_URL = os.getenv(
    "DATABASE_APP_URL",
    "postgresql://postgres:postgres@localhost:5432/footballapp_db"
)

engine = create_engine(DATABASE_APP_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency FastAPI — session vers footballapp_db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
