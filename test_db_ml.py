import sqlalchemy
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path

# Charge le .env à la racine
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DATABASE_ML_URL", "postgresql://localhost/footballml_db")
print(f"Testing connection to: {db_url}")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("Connection successful!")
        result = conn.execute(sqlalchemy.text("SELECT count(*) FROM team"))
        print(f"Teams count: {result.scalar()}")
except Exception as e:
    print(f"Connection failed: {e}")
