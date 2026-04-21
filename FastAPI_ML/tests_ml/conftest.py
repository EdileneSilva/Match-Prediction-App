"""
Shared fixtures for the entire test suite.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock


@pytest.fixture
def sample_matches_df():
    """Minimal DataFrame with the structure produced by _clean()."""
    return pd.DataFrame({
        "Date":      pd.to_datetime(["2024-01-10", "2024-01-17", "2024-01-24",
                                     "2024-02-01", "2024-02-08"]),
        "HomeTeam":  ["Paris SG", "Lyon",      "Marseille", "Lens",    "Nice"],
        "AwayTeam":  ["Lyon",     "Marseille", "Lens",      "Nice",    "Paris SG"],
        "HomeScore": [2, 1, 3, 0, 1],
        "AwayScore": [0, 1, 1, 2, 2],
        "Result":    ["H", "D", "H", "A", "A"],
        "HalftimeHomeGoals": [1, 0, 1, 0, 0],
        "HalftimeAwayGoals": [0, 0, 0, 1, 1],
        "HalftimeResult":    ["H", "D", "H", "A", "A"],
        "HomeShot":          [12, 8, 15, 5, 7],
        "AwayShot":          [5,  9,  6, 10, 11],
        "HomeShotTarget":    [5, 3, 7, 2, 3],
        "AwayShotTarget":    [2, 4, 2, 5, 5],
        "HomeTeamFouls":     [10, 12,  8, 14, 11],
        "AwayTeamFouls":     [11,  9, 13,  8, 10],
        "HomeTeamCorners":   [6, 4, 8, 2, 3],
        "AwayTeamCorners":   [3, 5, 3, 7, 6],
        "HomeYellowCards":   [2, 1, 0, 3, 1],
        "AwayYellowCards":   [1, 2, 1, 0, 2],
        "HomeRedCards":      [0, 0, 0, 0, 0],
        "AwayRedCards":      [0, 0, 0, 0, 0],
        "league.season":     [2024, 2024, 2024, 2024, 2024],
    })


@pytest.fixture
def sample_stats_df(sample_matches_df):
    """DataFrame with season stats and rolling features already computed."""
    from app.services.preparation import PreparationService
    svc = PreparationService()
    df  = svc._add_season_stats(sample_matches_df.copy())
    df  = svc._add_rolling_features(df)
    return df


@pytest.fixture
def training_df():
    """DataFrame with the structure returned by _load_from_db."""
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
    """MLService with reference stat DataFrames already loaded."""
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
