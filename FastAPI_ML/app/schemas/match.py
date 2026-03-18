from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MatchBase(BaseModel):
    date: datetime
    home_team_id: int
    away_team_id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    result: Optional[str] = None


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PredictionRequest(BaseModel):
    home_team_id: int
    away_team_id: int


class PredictionResponse(BaseModel):
    home_team_id: int
    away_team_id: int
    predicted_result: str  # e.g., "HOME_WIN", "AWAY_WIN", "DRAW"
    confidence_score: float

