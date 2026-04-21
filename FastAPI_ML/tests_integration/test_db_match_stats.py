"""
Integration tests — MatchStats model (PostgreSQL)
"""
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.match import MatchStats, FootballMatch

pytestmark = pytest.mark.integration


@pytest.fixture
def match_stats(db, match_psg_lyon):
    stats = MatchStats(
        match_id                 = match_psg_lyon.id,
        home_goals_scored_home   = 2.5,
        home_goals_conceded_home = 0.8,
        home_win_rate_home       = 0.75,
        away_goals_scored_away   = 1.2,
        away_goals_conceded_away = 1.5,
        away_win_rate_away       = 0.30,
        home_season_rank         = 1,
        away_season_rank         = 5,
        home_rolling_scored      = 2.2,
        home_rolling_conceded    = 0.6,
        home_rolling_win_rate    = 0.8,
        away_rolling_scored      = 1.1,
        away_rolling_conceded    = 1.4,
        away_rolling_win_rate    = 0.2,
    )
    db.add(stats)
    db.flush()
    return stats


class TestMatchStatsModel:

    def test_insert_match_stats(self, db, match_stats):
        assert match_stats.id is not None

    def test_stats_linked_to_match(self, db, match_stats, match_psg_lyon):
        fetched = db.query(MatchStats).filter_by(id=match_stats.id).first()
        assert fetched.match_id == match_psg_lyon.id

    def test_home_goals_scored_persisted(self, db, match_stats):
        fetched = db.query(MatchStats).filter_by(id=match_stats.id).first()
        assert fetched.home_goals_scored_home == 2.5

    def test_away_win_rate_persisted(self, db, match_stats):
        fetched = db.query(MatchStats).filter_by(id=match_stats.id).first()
        assert fetched.away_win_rate_away == 0.30

    def test_season_ranks_persisted(self, db, match_stats):
        fetched = db.query(MatchStats).filter_by(id=match_stats.id).first()
        assert fetched.home_season_rank == 1
        assert fetched.away_season_rank == 5

    def test_rolling_features_persisted(self, db, match_stats):
        fetched = db.query(MatchStats).filter_by(id=match_stats.id).first()
        assert fetched.home_rolling_scored   == 2.2
        assert fetched.home_rolling_conceded == 0.6
        assert fetched.home_rolling_win_rate == 0.8
        assert fetched.away_rolling_scored   == 1.1
        assert fetched.away_rolling_conceded == 1.4
        assert fetched.away_rolling_win_rate == 0.2

    def test_match_relationship(self, db, match_stats, match_psg_lyon):
        fetched = db.query(MatchStats).filter_by(id=match_stats.id).first()
        assert fetched.match.id == match_psg_lyon.id

    def test_match_stats_backref(self, db, match_stats, match_psg_lyon):
        fetched_match = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched_match.stats is not None
        assert fetched_match.stats.id == match_stats.id

    def test_unique_constraint_match_id(self, db, match_psg_lyon, match_stats):
        """Each match can have only one MatchStats row."""
        from sqlalchemy.exc import IntegrityError
        duplicate = MatchStats(
            match_id             = match_psg_lyon.id,
            home_goals_scored_home = 1.0,
        )
        db.add(duplicate)
        with pytest.raises(IntegrityError):
            db.flush()

    def test_cascade_delete_on_match(self, db, match_stats, match_psg_lyon, team_psg, team_lyon):
        """Deleting a FootballMatch must cascade-delete its MatchStats (ondelete=CASCADE).
        Uses raw SQL to bypass the ORM and let Postgres execute the CASCADE directly."""
        from sqlalchemy import text
        stats_id = match_stats.id
        match_id = match_psg_lyon.id
        db.execute(text("DELETE FROM football_matches WHERE id = :id"), {"id": match_id})
        db.flush()
        remaining = db.query(MatchStats).filter_by(id=stats_id).first()
        assert remaining is None
