import sys
from pathlib import Path
from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

# Ajout du chemin racine pour importer le package 'shared'
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.config.base_settings import CommonSettings

class Settings(CommonSettings):
    PROJECT_NAME: str = "Match Prediction App - Application API"
    
    # On mappe DATABASE_APP_URL ou DATABASE_URL
    DATABASE_URL: str = Field(
        default="postgresql://localhost/footballapp_db",
        validation_alias=AliasChoices("DATABASE_APP_URL", "DATABASE_URL"),
    )
    
    CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8082",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    ML_API_URL: str = Field(default="http://localhost:8001")

settings = Settings()
