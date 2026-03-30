import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Match Prediction App - ML API"
    PROJECT_VERSION: str = "0.1.0"
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_ML_URL", 
        "sqlite:///./ml_app.db"
    )
    
    CORS_ORIGINS: list = ["*"]
    DATA_DIR: str = os.getenv("DATA_DIR", "../Data/dataset")
    MODEL_PATH:   str = os.getenv("MODEL_PATH",   "model/match_model_v1.joblib")
    DATASET_PATH: str = os.getenv("DATASET_PATH", "model/football_stats_reference.csv")

settings = Settings()
