from pydantic import BaseModel
from typing import Union

class PredictionRequest(BaseModel):
    home_team_id: int
    away_team_id: int
    referee: str
    season: Union[str, int]
    round: int

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
