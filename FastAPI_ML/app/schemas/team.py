from typing import Optional
from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

