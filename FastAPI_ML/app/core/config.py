import sys
from pathlib import Path

from pydantic import AliasChoices, Field

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.config.base_settings import CommonSettings


class Settings(CommonSettings):
    PROJECT_NAME: str = "Match Prediction App - ML API"

    # On mappe automatiquement :
    # - `DATABASE_ML_URL` (nouvelle convention)
    # - `DATABASE_URL` (ancienne convention)
    DATABASE_URL: str = Field(
        default="postgresql://localhost/footballml_db",
        validation_alias=AliasChoices("DATABASE_ML_URL", "DATABASE_URL"),
    )

    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
