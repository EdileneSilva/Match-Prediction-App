"""
Unit tests — app/services/preparation.py
"""
import pytest
import pandas as pd
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.preparation import PreparationService


@pytest.fixture
def svc():
    return PreparationService()


@pytest.fixture
def raw_ext_df():
    """Simulates a football-data.co.uk CSV before harmonisation."""
    return pd.DataFrame({
        "Date":     ["10/01/2024", "17/01/2024"],
        "HomeTeam": ["Paris SG",   "Brest"],
        "AwayTeam": ["Lyon",       "Troyes"],
        "FTHG": [2, 1], "FTAG": [0, 1], "FTR": ["H", "D"],
        "HS": [12, 8],  "AS": [5, 9],
        "HST": [5, 3],  "AST": [2, 4],
        "HTHG": [1, 0], "HTAG": [0, 0], "HTR": ["H", "D"],
        "HF": [10, 12], "AF": [11, 9],
        "HC": [6, 4],   "AC": [3, 5],
        "HY": [2, 1],   "AY": [1, 2],
        "HR": [0, 0],   "AR": [0, 0],
    })


# ---------------------------------------------------------------------------
# Points helper methods
# ---------------------------------------------------------------------------

class TestPointsMethods:

    def test_home_win_gives_3_points(self, svc):
        assert svc._home_points("H") == 3

    def test_home_draw_gives_1_point(self, svc):
        assert svc._home_points("D") == 1

    def test_home_loss_gives_0_points(self, svc):
        assert svc._home_points("A") == 0

    def test_away_win_gives_3_points(self, svc):
        assert svc._away_points("A") == 3

    def test_away_draw_gives_1_point(self, svc):
        assert svc._away_points("D") == 1

    def test_away_loss_gives_0_points(self, svc):
        assert svc._away_points("H") == 0


# ---------------------------------------------------------------------------
# _harmonise_ext
# ---------------------------------------------------------------------------

class TestHarmoniseExt:

    def test_renames_score_columns(self, svc, raw_ext_df):
        result = svc._harmonise_ext(raw_ext_df.copy())
        assert "HomeScore" in result.columns
        assert "AwayScore" in result.columns
        assert "FTHG" not in result.columns

    def test_renames_result_column(self, svc, raw_ext_df):
        result = svc._harmonise_ext(raw_ext_df.copy())
        assert "Result" in result.columns

    def test_normalises_brest(self, svc, raw_ext_df):
        result = svc._harmonise_ext(raw_ext_df.copy())
        assert "Stade Brestois" in result["HomeTeam"].values

    def test_normalises_troyes(self, svc, raw_ext_df):
        result = svc._harmonise_ext(raw_ext_df.copy())
        assert "Estac Troyes" in result["AwayTeam"].values


# ---------------------------------------------------------------------------
# _clean
# ---------------------------------------------------------------------------

class TestClean:

    def test_removes_rows_without_result(self, svc, sample_matches_df):
        df = sample_matches_df.copy()
        df.loc[0, "Result"] = None
        result = svc._clean(df)
        assert len(result) == len(sample_matches_df) - 1

    def test_fills_missing_league_season(self, svc, sample_matches_df):
        df = sample_matches_df.copy()
        df["league.season"] = None
        result = svc._clean(df)
        assert result["league.season"].notna().all()

    def test_drops_betting_columns(self, svc, sample_matches_df):
        df = sample_matches_df.copy()
        df["B365H"] = 1.5
        df["PSH"]   = 1.6
        result = svc._clean(df)
        assert "B365H" not in result.columns
        assert "PSH"   not in result.columns

    def test_sorted_by_date(self, svc, sample_matches_df):
        df = sample_matches_df.sample(frac=1, random_state=42)
        result = svc._clean(df)
        assert result["Date"].is_monotonic_increasing

    def test_keeps_all_valid_rows(self, svc, sample_matches_df):
        result = svc._clean(sample_matches_df.copy())
        assert len(result) == len(sample_matches_df)

    def test_league_season_is_integer(self, svc, sample_matches_df):
        result = svc._clean(sample_matches_df.copy())
        assert result["league.season"].dtype in [int, "int64", "int32"]


# ---------------------------------------------------------------------------
# _add_season_stats
# ---------------------------------------------------------------------------

class TestAddSeasonStats:

    def test_adds_home_goals_scored(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert "home_goals_scored_home" in result.columns

    def test_adds_away_goals_scored(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert "away_goals_scored_away" in result.columns

    def test_adds_win_rates(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert "home_win_rate_home" in result.columns
        assert "away_win_rate_away" in result.columns

    def test_adds_season_rank(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert "home_season_rank" in result.columns
        assert "away_season_rank" in result.columns

    def test_win_rate_between_0_and_1(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert result["home_win_rate_home"].between(0, 1).all()
        assert result["away_win_rate_away"].between(0, 1).all()

    def test_season_rank_is_positive(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert (result["home_season_rank"] >= 1).all()

    def test_row_count_unchanged(self, svc, sample_matches_df):
        result = svc._add_season_stats(sample_matches_df.copy())
        assert len(result) == len(sample_matches_df)


# ---------------------------------------------------------------------------
# _add_rolling_features
# ---------------------------------------------------------------------------

class TestAddRollingFeatures:

    def test_adds_all_six_rolling_columns(self, svc, sample_matches_df):
        stats  = svc._add_season_stats(sample_matches_df.copy())
        result = svc._add_rolling_features(stats)
        for col in [
            "home_rolling_scored",   "home_rolling_conceded", "home_rolling_win_rate",
            "away_rolling_scored",   "away_rolling_conceded", "away_rolling_win_rate",
        ]:
            assert col in result.columns, f"Missing column: {col}"

    def test_no_data_leakage_on_first_match(self, svc, sample_matches_df):
        """First match per team must have rolling = 0 due to shift(1)."""
        stats  = svc._add_season_stats(sample_matches_df.copy())
        result = svc._add_rolling_features(stats)
        first_psg = result[result["HomeTeam"] == "Paris SG"].iloc[0]
        assert first_psg["home_rolling_scored"] == 0.0

    def test_rolling_values_are_non_negative(self, svc, sample_matches_df):
        stats  = svc._add_season_stats(sample_matches_df.copy())
        result = svc._add_rolling_features(stats)
        assert (result["home_rolling_scored"] >= 0).all()
        assert (result["away_rolling_scored"] >= 0).all()

    def test_row_count_unchanged(self, svc, sample_matches_df):
        stats  = svc._add_season_stats(sample_matches_df.copy())
        result = svc._add_rolling_features(stats)
        assert len(result) == len(sample_matches_df)

    def test_accepts_custom_window(self, svc, sample_matches_df):
        stats  = svc._add_season_stats(sample_matches_df.copy())
        result = svc._add_rolling_features(stats, window=3)
        assert "home_rolling_scored" in result.columns
