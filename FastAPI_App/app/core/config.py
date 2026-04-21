import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Charge .env depuis la racine du projet (un niveau au-dessus de FastAPI_App/)
_root_env = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=_root_env)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Match Prediction App - Application API"
    PROJECT_VERSION: str = "0.1.0"

    # Aucune valeur par défaut : une mauvaise config lève une erreur au démarrage
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ML_API_URL: str = "http://localhost:8001"

    class Config:
        env_file = str(_root_env)
        env_file_encoding = "utf-8"
        extra = "ignore"  # Le .env est partagé — on ignore les vars des autres services


settings = Settings()
