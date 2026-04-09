"""
Unit tests — app/services/ml_service.py
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.ml_service import MLService


@pytest.fixture
def svc():
    return MLService()


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

class TestMLServiceInit:

    def test_model_not_loaded_on_init(self, svc):
        assert svc.is_model_loaded is False

    def test_model_is_none_on_init(self, svc):
        assert svc.model is None

    def test_all_stat_frames_are_none(self, svc):
        assert svc.home_stats   is None
        assert svc.away_stats   is None
        assert svc.standings    is None
        assert svc.rolling_home is None
        assert svc.rolling_away is None


# ---------------------------------------------------------------------------
# load_model
# ---------------------------------------------------------------------------

class TestLoadModel:

    def test_sets_is_model_loaded_to_true(self, svc, tmp_path):
        import joblib
        from sklearn.dummy import DummyClassifier
        joblib.dump(DummyClassifier(), tmp_path / "model.joblib")
        with patch("app.services.ml_service.settings") as m:
            m.MODEL_PATH = str(tmp_path / "model.joblib")
            svc.load_model()
        assert svc.is_model_loaded is True

    def test_stays_false_when_file_missing(self, svc, tmp_path):
        with patch("app.services.ml_service.settings") as m:
            m.MODEL_PATH = str(tmp_path / "nonexistent.joblib")
            svc.load_model()
        assert svc.is_model_loaded is False


# ---------------------------------------------------------------------------
# get_stat
# ---------------------------------------------------------------------------

class TestGetStat:

    def test_returns_correct_value(self, populated_ml_service):
        val = populated_ml_service.get_stat(
            "Paris SG", 2024, "goals_scored_home", populated_ml_service.home_stats)
        assert val == 2.5

    def test_returns_zero_for_unknown_team(self, populated_ml_service):
        val = populated_ml_service.get_stat(
            "Unknown FC", 2024, "goals_scored_home", populated_ml_service.home_stats)
        assert val == 0.0

    def test_returns_zero_for_unknown_season(self, populated_ml_service):
        val = populated_ml_service.get_stat(
            "Paris SG", 1999, "goals_scored_home", populated_ml_service.home_stats)
        assert val == 0.0

    def test_returns_win_rate(self, populated_ml_service):
        val = populated_ml_service.get_stat(
            "Lyon", 2024, "win_rate_home", populated_ml_service.home_stats)
        assert val == 0.40

    def test_returns_season_rank(self, populated_ml_service):
        val = populated_ml_service.get_stat(
            "Paris SG", 2024, "season_rank", populated_ml_service.standings)
        assert val == 1


# ---------------------------------------------------------------------------
# _build_input
# ---------------------------------------------------------------------------

class TestBuildInput:

    def test_returns_dataframe(self, populated_ml_service):
        df = populated_ml_service._build_input("Paris SG", "Lyon", 2024)
        assert isinstance(df, pd.DataFrame)

    def test_has_exactly_one_row(self, populated_ml_service):
        df = populated_ml_service._build_input("Paris SG", "Lyon", 2024)
        assert len(df) == 1

    def test_contains_all_numeric_features(self, populated_ml_service):
        df = populated_ml_service._build_input("Paris SG", "Lyon", 2024)
        for col in [
            "home_goals_scored_home", "home_goals_conceded_home", "home_win_rate_home",
            "away_goals_scored_away", "away_goals_conceded_away", "away_win_rate_away",
            "home_season_rank", "away_season_rank",
            "home_rolling_scored", "home_rolling_conceded", "home_rolling_win_rate",
            "away_rolling_scored", "away_rolling_conceded", "away_rolling_win_rate",
            "league_season",
        ]:
            assert col in df.columns, f"Missing column: {col}"

    def test_contains_team_name_columns(self, populated_ml_service):
        df = populated_ml_service._build_input("Paris SG", "Lyon", 2024)
        assert "HomeTeam" in df.columns
        assert "AwayTeam" in df.columns

    def test_team_names_are_correct(self, populated_ml_service):
        df = populated_ml_service._build_input("Paris SG", "Lyon", 2024)
        assert df.iloc[0]["HomeTeam"] == "Paris SG"
        assert df.iloc[0]["AwayTeam"] == "Lyon"

    def test_unknown_team_returns_zeros(self, populated_ml_service):
        df = populated_ml_service._build_input("Unknown FC", "Lyon", 2024)
        assert df.iloc[0]["home_goals_scored_home"] == 0.0


# ---------------------------------------------------------------------------
# predict_match
# ---------------------------------------------------------------------------

class TestPredictMatch:

    def _mock_model(self, probs):
        m = MagicMock()
        m.predict_proba.return_value = np.array([probs])
        return m

    def test_predicts_home_win(self, populated_ml_service):
        populated_ml_service.model           = self._mock_model([0.1, 0.2, 0.7])
        populated_ml_service.is_model_loaded = True
        assert populated_ml_service.predict_match("Paris SG", "Lyon", 2024)["prediction"] == "HOME_WIN"

    def test_predicts_away_win(self, populated_ml_service):
        populated_ml_service.model           = self._mock_model([0.7, 0.2, 0.1])
        populated_ml_service.is_model_loaded = True
        assert populated_ml_service.predict_match("Paris SG", "Lyon", 2024)["prediction"] == "AWAY_WIN"

    def test_predicts_draw(self, populated_ml_service):
        populated_ml_service.model           = self._mock_model([0.2, 0.6, 0.2])
        populated_ml_service.is_model_loaded = True
        assert populated_ml_service.predict_match("Paris SG", "Lyon", 2024)["prediction"] == "DRAW"

    def test_probabilities_sum_to_one(self, populated_ml_service):
        populated_ml_service.model           = self._mock_model([0.3, 0.3, 0.4])
        populated_ml_service.is_model_loaded = True
        result = populated_ml_service.predict_match("Paris SG", "Lyon", 2024)
        assert abs(sum(result["probabilities"].values()) - 1.0) < 1e-6

    def test_confidence_equals_max_probability(self, populated_ml_service):
        probs = [0.2, 0.3, 0.5]
        populated_ml_service.model           = self._mock_model(probs)
        populated_ml_service.is_model_loaded = True
        result = populated_ml_service.predict_match("Paris SG", "Lyon", 2024)
        assert result["confidence"] == round(max(probs), 4)

    def test_result_contains_all_keys(self, populated_ml_service):
        populated_ml_service.model           = self._mock_model([0.3, 0.3, 0.4])
        populated_ml_service.is_model_loaded = True
        result = populated_ml_service.predict_match("Paris SG", "Lyon", 2024)
        for key in ["match", "prediction", "confidence", "probabilities"]:
            assert key in result

    def test_match_label_is_correct(self, populated_ml_service):
        populated_ml_service.model           = self._mock_model([0.3, 0.3, 0.4])
        populated_ml_service.is_model_loaded = True
        result = populated_ml_service.predict_match("Paris SG", "Lyon", 2024)
        assert result["match"] == "Paris SG vs Lyon"
