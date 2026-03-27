from pydantic import BaseModel
from typing import Union

class PredictionRequest(BaseModel):
    home_team_id: int
    away_team_id: int
    referee: str = "TBD"
    season: Union[str, int] = "2023-24"
    round: int = 1

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
