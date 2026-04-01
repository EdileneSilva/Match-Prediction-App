import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Match Prediction App - Application API"
    PROJECT_VERSION: str = "0.1.0"
    
    DATABASE_URL: str = "postgresql://slyxi@/footballapp_db"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: list = ["http://localhost:3000"]

settings = Settings()
