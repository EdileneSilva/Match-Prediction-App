from pydantic import BaseModel


class PredictionRequest(BaseModel):
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str


class PredictionResponse(BaseModel):
    predicted_result: str
    confidence_score: float

