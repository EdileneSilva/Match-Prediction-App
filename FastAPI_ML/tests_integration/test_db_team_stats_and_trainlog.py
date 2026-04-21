"""
Integration tests — TeamStatsReference and TrainLog models (PostgreSQL)
"""
import pytest
from datetime import datetime, timezone
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.match import TeamStatsReference, TrainLog

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# TeamStatsReference
# ---------------------------------------------------------------------------

@pytest.fixture
def psg_stats(db):
    stats = TeamStatsReference(
        team   = "Paris SG",
        season = 2024,
        goals_scored_home   = 2.5,
        goals_conceded_home = 0.8,
        win_rate_home       = 0.75,
        goals_scored_away   = 1.8,
        goals_conceded_away = 1.0,
        win_rate_away       = 0.55,
        season_rank         = 1.0,
        rolling_scored_home   = 2.2,
        rolling_conceded_home = 0.6,
        rolling_win_rate_home = 0.8,
        rolling_scored_away   = 1.6,
        rolling_conceded_away = 0.9,
        rolling_win_rate_away = 0.6,
    )
    db.add(stats)
    db.flush()
    return stats


class TestTeamStatsReference:

    def test_insert_team_stats(self, db, psg_stats):
        assert psg_stats.id is not None

    def test_team_name_persisted(self, db, psg_stats):
        fetched = db.query(TeamStatsReference).filter_by(id=psg_stats.id).first()
        assert fetched.team == "Paris SG"

    def test_season_persisted(self, db, psg_stats):
        fetched = db.query(TeamStatsReference).filter_by(id=psg_stats.id).first()
        assert fetched.season == 2024

    def test_home_stats_persisted(self, db, psg_stats):
        fetched = db.query(TeamStatsReference).filter_by(id=psg_stats.id).first()
        assert fetched.goals_scored_home   == 2.5
        assert fetched.goals_conceded_home == 0.8
        assert fetched.win_rate_home       == 0.75

    def test_away_stats_persisted(self, db, psg_stats):
        fetched = db.query(TeamStatsReference).filter_by(id=psg_stats.id).first()
        assert fetched.goals_scored_away   == 1.8
        assert fetched.goals_conceded_away == 1.0
        assert fetched.win_rate_away       == 0.55

    def test_season_rank_persisted(self, db, psg_stats):
        fetched = db.query(TeamStatsReference).filter_by(id=psg_stats.id).first()
        assert fetched.season_rank == 1.0

    def test_rolling_stats_persisted(self, db, psg_stats):
        fetched = db.query(TeamStatsReference).filter_by(id=psg_stats.id).first()
        assert fetched.rolling_scored_home   == 2.2
        assert fetched.rolling_win_rate_away == 0.6

    def test_filter_by_team_and_season(self, db, psg_stats):
        result = db.query(TeamStatsReference).filter_by(
            team="Paris SG", season=2024).first()
        assert result is not None

    def test_multiple_teams_same_season(self, db):
        db.add(TeamStatsReference(team="Lyon",      season=2024, season_rank=5.0))
        db.add(TeamStatsReference(team="Marseille", season=2024, season_rank=3.0))
        db.flush()
        count = db.query(TeamStatsReference).filter_by(season=2024).count()
        assert count >= 2

    def test_delete_by_season(self, db, psg_stats):
        db.query(TeamStatsReference).filter_by(season=2024).delete()
        db.flush()
        remaining = db.query(TeamStatsReference).filter_by(season=2024).first()
        assert remaining is None

    def test_updated_at_set_automatically(self, db, psg_stats):
        assert psg_stats.updated_at is not None


# ---------------------------------------------------------------------------
# TrainLog
# ---------------------------------------------------------------------------

@pytest.fixture
def train_log(db):
    log = TrainLog(
        model_version = "20240101",
        n_samples     = 500,
        cv_accuracy   = 0.65,
        cv_log_loss   = 0.88,
        status        = "success",
    )
    db.add(log)
    db.flush()
    return log


class TestTrainLog:

    def test_insert_train_log(self, db, train_log):
        assert train_log.id is not None

    def test_model_version_persisted(self, db, train_log):
        fetched = db.query(TrainLog).filter_by(id=train_log.id).first()
        assert fetched.model_version == "20240101"

    def test_metrics_persisted(self, db, train_log):
        fetched = db.query(TrainLog).filter_by(id=train_log.id).first()
        assert fetched.n_samples   == 500
        assert fetched.cv_accuracy == 0.65
        assert fetched.cv_log_loss == 0.88

    def test_status_persisted(self, db, train_log):
        fetched = db.query(TrainLog).filter_by(id=train_log.id).first()
        assert fetched.status == "success"

    def test_created_at_set_automatically(self, db, train_log):
        assert train_log.created_at is not None

    def test_error_message_is_none_on_success(self, db, train_log):
        fetched = db.query(TrainLog).filter_by(id=train_log.id).first()
        assert fetched.error_message is None

    def test_error_message_persisted_on_failure(self, db):
        log = TrainLog(
            model_version = "20240102",
            n_samples     = 0,
            cv_accuracy   = 0.0,
            cv_log_loss   = 0.0,
            status        = "error",
            error_message = "No data available",
        )
        db.add(log)
        db.flush()
        fetched = db.query(TrainLog).filter_by(id=log.id).first()
        assert fetched.error_message == "No data available"
        assert fetched.status        == "error"

    def test_order_by_created_at_desc(self, db):
        for version in ["20240101", "20240102", "20240103"]:
            db.add(TrainLog(
                model_version=version, n_samples=100,
                cv_accuracy=0.6, cv_log_loss=0.9, status="success"))
        db.flush()
        logs = db.query(TrainLog).order_by(TrainLog.created_at.desc()).limit(3).all()
        assert len(logs) == 3

    def test_limit_query(self, db):
        for i in range(5):
            db.add(TrainLog(
                model_version=f"2024010{i}", n_samples=100,
                cv_accuracy=0.6, cv_log_loss=0.9, status="success"))
        db.flush()
        logs = db.query(TrainLog).limit(2).all()
        assert len(logs) <= 2
