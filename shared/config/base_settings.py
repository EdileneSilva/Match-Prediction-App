from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Chemin vers la racine du projet (Match-Prediction-App/)
ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = ROOT_DIR / ".env"


class CommonSettings(BaseSettings):
    """
    Settings communs aux services (env_file unique, JWT, etc.).
    Chaque API étend cette classe pour ajouter ses champs spécifiques.
    """

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else None,
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_VERSION: str = "0.1.0"

    # JWT (utilisé par l'API Application; présent ici pour éviter la duplication)
    SECRET_KEY: str = "your-super-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

