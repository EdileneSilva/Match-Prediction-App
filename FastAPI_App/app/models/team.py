from sqlalchemy import Column, Integer, String
from ..database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    short_name = Column(String, unique=True, index=True, nullable=False)
    logo_url = Column(String, nullable=True)
