import sys
from pathlib import Path
from pydantic import AliasChoices, Field
import os

# Ajout du chemin racine pour importer le package 'shared'
# In Docker, shared is at /app/shared, not relative to this file
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.config.base_settings import CommonSettings

class Settings(CommonSettings):
    PROJECT_NAME: str = "Match Prediction App - ML API"
    
    # Database configuration
    # On mappe DATABASE_ML_URL vers DATABASE_URL pour compatibilite avec BaseSettings
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@postgres:5432/footballml_db",
        validation_alias=AliasChoices("DATABASE_ML_URL", "DATABASE_URL"),
    )
    
    # CORS - simple string list, no env parsing needed
    CORS_ORIGINS: list = ["*"]
    DATA_DIR: str = Field(default="/app/Data/dataset/")
    MODEL_PATH: str = Field(default="/app/Data/dataset/match_model_v1.joblib")
    DATASET_PATH: str = Field(default="/app/Data/dataset/completed_match_dataset_final.csv")
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "sqlite:////app/mlflow.db")
    
    # Server configuration
    ML_HOST: str = "0.0.0.0"
    ML_PORT: int = 8001
    ML_DEBUG: bool = True

settings = Settings()

# Ensure DATABASE_URL is properly set for Docker
if os.getenv("DATABASE_ML_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_ML_URL")
if os.getenv("DATABASE_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_URL")
