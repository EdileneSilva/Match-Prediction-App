from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


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
    home_team_name: str
    home_team_logo_url: Optional[str] = None
    away_team_name: str
    away_team_logo_url: Optional[str] = None
    predicted_result: Optional[str]
    confidence_score: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserFavoriteTeamBase(BaseModel):
    team_name: str


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
