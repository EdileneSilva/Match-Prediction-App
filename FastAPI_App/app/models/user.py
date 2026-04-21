from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    prediction_history = relationship("PredictionHistory", back_populates="user", cascade="all, delete-orphan")
    favorite_teams = relationship("UserFavoriteTeam", back_populates="user", cascade="all, delete-orphan")


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    home_team_name = Column(String(100), nullable=False)
    home_team_logo_url = Column(Text, nullable=True)
    away_team_name = Column(String(100), nullable=False)
    away_team_logo_url = Column(Text, nullable=True)
    predicted_result = Column(String(10), nullable=True)
    confidence_score = Column(Numeric(5, 4), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="prediction_history")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])


class UserFavoriteTeam(Base):
    __tablename__ = "user_favorite_team"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)   # FK optionnel (develop)

    user = relationship("User", back_populates="favorite_teams")

