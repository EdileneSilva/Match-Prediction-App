from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# -- Teams --
class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# -- Matches --
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

# -- Stats --
class TeamMatchStatsBase(BaseModel):
    match_id: int
    team_id: int
    is_home: Optional[bool] = None
    goals: Optional[int] = None
    shots: Optional[int] = None
    shots_on_target: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None
    corners: Optional[int] = None
    fouls: Optional[int] = None

class TeamMatchStatsCreate(TeamMatchStatsBase):
    pass

class TeamMatchStats(TeamMatchStatsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
