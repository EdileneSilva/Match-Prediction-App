from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

_MIN_PASSWORD_LENGTH = 8
_MAX_PASSWORD_LENGTH = 72  # bcrypt silently truncates beyond 72 bytes


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < _MIN_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {_MIN_PASSWORD_LENGTH} characters.")
        if len(v.encode("utf-8")) > _MAX_PASSWORD_LENGTH:
            raise ValueError(f"Password must not exceed {_MAX_PASSWORD_LENGTH} bytes.")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if len(v) > 50:
            raise ValueError("Username must not exceed 50 characters.")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionHistoryOut(BaseModel):
    id: int
    user_id: int
    home_team_id: int
    away_team_id: int
    home_team_name: str
    home_team_logo_url: Optional[str] = None
    away_team_name: str
    away_team_logo_url: Optional[str] = None
    predicted_result: Optional[str]
    confidence_score: Optional[float]
    created_at: datetime
    actual_result: Optional[str] = None
    actual_home_goals: Optional[int] = None
    actual_away_goals: Optional[int] = None
    gameweek: Optional[int] = None
    is_correct: Optional[bool] = None
    probability_actual_result: Optional[float] = None
    proximity_score: Optional[float] = None
    proximity_status: Optional[str] = "unknown"

    model_config = ConfigDict(from_attributes=True)


class UserFavoriteTeamBase(BaseModel):
    team_id: int


class UserFavoriteTeamOut(UserFavoriteTeamBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserStats(BaseModel):
    total_predictions: int
    favorite_teams_count: int
    # On pourrait ajouter win_rate si on avait les résultats réels


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str
