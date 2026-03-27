from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    name: str
    short_name: str
    logo_url: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int

    class Config:
        from_attributes = True
