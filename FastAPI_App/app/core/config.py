import os
import sys
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

_INSECURE_SECRET_KEYS = {
    "your-super-secret-key-change-me-in-production",
    "your-super-secret-key-change-me",
    "secret",
    "changeme",
}


class Settings(BaseSettings):
    """Application API Settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Project info
    PROJECT_NAME: str = "Match Prediction App - Application API"
    PROJECT_VERSION: str = "0.1.0"

    # Database configuration
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@postgres:5432/footballapp_db",
        alias="DATABASE_APP_URL",
    )

    # JWT Authentication
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-me-in-production",
        description="JWT secret key for authentication",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS Configuration - accept as string and parse
    CORS_ORIGINS_ENV: Optional[str] = Field(
        default=None,
        alias="CORS_ORIGINS",
        description="Comma-separated list of allowed CORS origins",
    )

    @field_validator("CORS_ORIGINS_ENV", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return v
        return v

    @property
    def CORS_ORIGINS(self) -> List[str]:
        if self.CORS_ORIGINS_ENV:
            return [origin.strip() for origin in self.CORS_ORIGINS_ENV.split(",")]
        return [
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
        ]

    # ML API URL and shared API key
    ML_API_URL: str = Field(
        default="http://ml-api:8001",
        description="URL of the ML API service",
    )
    ML_API_KEY: str = Field(
        default="",
        description="Shared API key for authenticating requests to the ML API",
    )

    # Server configuration
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = False


# Create settings instance
settings = Settings()

# Ensure ML_API_URL is properly set for Docker
if os.getenv("ML_API_URL"):
    settings.ML_API_URL = os.getenv("ML_API_URL")
if os.getenv("ML_API_KEY"):
    settings.ML_API_KEY = os.getenv("ML_API_KEY")

# Ensure DATABASE_URL is properly set for Docker
if os.getenv("DATABASE_APP_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_APP_URL")
if os.getenv("DATABASE_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_URL")

# Refuse to start with a known-insecure secret key
if settings.SECRET_KEY.lower() in _INSECURE_SECRET_KEYS or len(settings.SECRET_KEY) < 32:
    print(
        "FATAL: SECRET_KEY is insecure or too short. "
        "Generate one with: python3 -c \"import secrets; print(secrets.token_hex(32))\""
    )
    sys.exit(1)
