import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Match Prediction App - ML API"
    PROJECT_VERSION: str = "0.1.0"
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_ML_URL", 
        "postgresql://localhost/footballml_db"
    )
    
    CORS_ORIGINS: list = ["*"]

settings = Settings()
