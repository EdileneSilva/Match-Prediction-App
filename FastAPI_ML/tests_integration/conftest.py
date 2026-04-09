"""
Integration test fixtures — requires a real PostgreSQL instance.

Set the environment variable before running:
    export DATABASE_ML_URL="postgresql://user:password@localhost:5432/test_footballml_db"

The test database must exist but will be fully wiped and recreated on each session.
Run with:
    pytest tests_integration/ -v -m integration
"""
import os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------
# Database URL — read from environment, never hardcoded
# ---------------------------------------------------------------------------

DATABASE_URL = os.environ.get(
    "DATABASE_ML_URL",
    "postgresql://postgres:postgres@localhost:5432/test_footballml_db",
)


@pytest.fixture(scope="session")
def pg_engine():
    """
    Creates the engine and all tables once per test session.
    Drops and recreates all tables to guarantee a clean state.
    """
    from app.database import Base
    # Import models so SQLAlchemy registers them on Base.metadata
    import app.models.match  # noqa: F401

    engine = create_engine(DATABASE_URL)

    # Full reset — drop then recreate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine

    # Teardown — drop all tables after the session ends
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db(pg_engine):
    """
    Provides a clean transactional session for each test.
    All changes are rolled back after the test — no data bleeds between tests.
    """
    connection  = pg_engine.connect()
    transaction = connection.begin()
    Session     = sessionmaker(bind=connection)
    session     = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ---------------------------------------------------------------------------
# Shared data helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def team_psg(db):
    from app.models.match import Team
    team = Team(name="Paris SG")
    db.add(team)
    db.flush()
    return team


@pytest.fixture
def team_lyon(db):
    from app.models.match import Team
    team = Team(name="Lyon")
    db.add(team)
    db.flush()
    return team


@pytest.fixture
def match_psg_lyon(db, team_psg, team_lyon):
    from app.models.match import FootballMatch
    match = FootballMatch(
        league_season = 2024,
        home_team_id  = team_psg.id,
        away_team_id  = team_lyon.id,
        home_score    = 3,
        away_score    = 1,
        date          = "2024-01-10",
        result        = "H",
        halftime_home_goals = 1,
        halftime_away_goals = 0,
        halftime_result     = "H",
        home_shot           = 14,
        away_shot           = 6,
        home_shot_target    = 6,
        away_shot_target    = 2,
        home_team_fouls     = 10,
        away_team_fouls     = 12,
        home_team_corners   = 7,
        away_team_corners   = 3,
        home_yellow_cards   = 1,
        away_yellow_cards   = 2,
        home_red_cards      = 0,
        away_red_cards      = 0,
    )
    db.add(match)
    db.flush()
    return match


# ---------------------------------------------------------------------------
# ML fixtures — needed by test_ml_service.py and test_pipeline_service.py
# ---------------------------------------------------------------------------

@pytest.fixture
def training_df():
    return pd.DataFrame({
        "league_season": [2024] * 10,
        "Result":        ["H", "D", "A", "H", "H", "D", "A", "H", "D", "A"],
        "HomeTeam":      ["Paris SG", "Lyon", "Marseille", "Lens", "Nice",
                          "Paris SG", "Lyon", "Marseille", "Lens", "Nice"],
        "AwayTeam":      ["Lyon", "Marseille", "Lens", "Nice", "Paris SG",
                          "Marseille", "Lens", "Nice", "Paris SG", "Lyon"],
        "home_goals_scored_home":   [2.5, 1.5, 1.8, 1.0, 1.2] * 2,
        "home_goals_conceded_home": [0.8, 1.2, 1.0, 1.5, 1.1] * 2,
        "home_win_rate_home":       [0.75, 0.4, 0.5, 0.3, 0.45] * 2,
        "away_goals_scored_away":   [1.8, 1.2, 1.0, 0.8, 1.5] * 2,
        "away_goals_conceded_away": [1.0, 1.5, 1.2, 1.8, 1.0] * 2,
        "away_win_rate_away":       [0.55, 0.3, 0.4, 0.2, 0.5] * 2,
        "home_season_rank":         [1, 5, 3, 8, 6] * 2,
        "away_season_rank":         [5, 3, 8, 6, 1] * 2,
        "home_rolling_scored":      [2.2, 1.4, 1.6, 0.8, 1.0] * 2,
        "home_rolling_conceded":    [0.6, 1.0, 0.8, 1.2, 1.1] * 2,
        "home_rolling_win_rate":    [0.8, 0.4, 0.6, 0.2, 0.4] * 2,
        "away_rolling_scored":      [1.6, 1.1, 0.9, 0.7, 1.3] * 2,
        "away_rolling_conceded":    [0.9, 1.4, 1.1, 1.6, 0.8] * 2,
        "away_rolling_win_rate":    [0.6, 0.2, 0.4, 0.1, 0.5] * 2,
    })


@pytest.fixture
def populated_ml_service():
    from app.services.ml_service import MLService
    s = MLService()
    s.home_stats = pd.DataFrame([
        {"league.season": 2024, "Team": "Paris SG", "goals_scored_home": 2.5,
         "goals_conceded_home": 0.8, "win_rate_home": 0.75},
        {"league.season": 2024, "Team": "Lyon",     "goals_scored_home": 1.5,
         "goals_conceded_home": 1.2, "win_rate_home": 0.40},
    ])
    s.away_stats = pd.DataFrame([
        {"league.season": 2024, "Team": "Paris SG", "goals_scored_away": 1.8,
         "goals_conceded_away": 1.0, "win_rate_away": 0.55},
        {"league.season": 2024, "Team": "Lyon",     "goals_scored_away": 1.2,
         "goals_conceded_away": 1.5, "win_rate_away": 0.30},
    ])
    s.standings = pd.DataFrame([
        {"league.season": 2024, "Team": "Paris SG", "season_rank": 1},
        {"league.season": 2024, "Team": "Lyon",     "season_rank": 5},
    ])
    s.rolling_home = pd.DataFrame([
        {"league.season": 2024, "Team": "Paris SG", "rolling_scored": 2.2,
         "rolling_conceded": 0.6, "rolling_win_rate": 0.8},
        {"league.season": 2024, "Team": "Lyon",     "rolling_scored": 1.4,
         "rolling_conceded": 1.0, "rolling_win_rate": 0.4},
    ])
    s.rolling_away = pd.DataFrame([
        {"league.season": 2024, "Team": "Paris SG", "rolling_scored": 1.6,
         "rolling_conceded": 0.9, "rolling_win_rate": 0.6},
        {"league.season": 2024, "Team": "Lyon",     "rolling_scored": 1.1,
         "rolling_conceded": 1.4, "rolling_win_rate": 0.2},
    ])
    return s
