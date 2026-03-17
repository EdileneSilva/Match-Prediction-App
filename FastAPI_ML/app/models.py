from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    statistics = relationship("TeamMatchStats", back_populates="team")


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, nullable=False)
    home_team_id = Column(Integer, ForeignKey("team.id", ondelete="RESTRICT"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("team.id", ondelete="RESTRICT"), nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    result = Column(String(10), nullable=True)

    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    statistics = relationship("TeamMatchStats", back_populates="match")


class TeamMatchStats(Base):
    __tablename__ = "team_match_stats"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("match.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("team.id", ondelete="RESTRICT"), nullable=False)
    is_home = Column(Boolean, nullable=True)
    goals = Column(Integer, nullable=True)
    shots = Column(Integer, nullable=True)
    shots_on_target = Column(Integer, nullable=True)
    yellow_cards = Column(Integer, nullable=True)
    red_cards = Column(Integer, nullable=True)
    corners = Column(Integer, nullable=True)
    fouls = Column(Integer, nullable=True)

    match = relationship("Match", back_populates="statistics")
    team = relationship("Team", back_populates="statistics")

