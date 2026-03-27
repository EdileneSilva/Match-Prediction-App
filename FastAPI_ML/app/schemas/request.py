from pydantic import BaseModel
from typing import Union

class MatchRequest(BaseModel):
    home_team: str
    away_team: str
    referee: str
    season: Union[str, int]
    round: int