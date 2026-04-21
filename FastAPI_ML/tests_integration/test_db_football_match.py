"""
Integration tests — FootballMatch model (PostgreSQL)
"""
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.match import FootballMatch, Team

pytestmark = pytest.mark.integration


class TestFootballMatchModel:

    def test_insert_match(self, db, match_psg_lyon):
        assert match_psg_lyon.id is not None

    def test_match_result_persisted(self, db, match_psg_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.result == "H"

    def test_match_scores_persisted(self, db, match_psg_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.home_score == 3
        assert fetched.away_score == 1

    def test_match_season_persisted(self, db, match_psg_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.league_season == 2024

    def test_match_has_home_team_relationship(self, db, match_psg_lyon, team_psg):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.home_team.name == "Paris SG"

    def test_match_has_away_team_relationship(self, db, match_psg_lyon, team_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.away_team.name == "Lyon"

    def test_team_home_matches_backref(self, db, match_psg_lyon, team_psg):
        assert len(team_psg.home_matches) == 1
        assert team_psg.home_matches[0].id == match_psg_lyon.id

    def test_team_away_matches_backref(self, db, match_psg_lyon, team_lyon):
        assert len(team_lyon.away_matches) == 1
        assert team_lyon.away_matches[0].id == match_psg_lyon.id

    def test_halftime_stats_persisted(self, db, match_psg_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.halftime_home_goals == 1
        assert fetched.halftime_away_goals == 0
        assert fetched.halftime_result     == "H"

    def test_shot_stats_persisted(self, db, match_psg_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.home_shot        == 14
        assert fetched.away_shot        == 6
        assert fetched.home_shot_target == 6
        assert fetched.away_shot_target == 2

    def test_card_stats_persisted(self, db, match_psg_lyon):
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.home_yellow_cards == 1
        assert fetched.away_yellow_cards == 2
        assert fetched.home_red_cards    == 0
        assert fetched.away_red_cards    == 0

    def test_match_stats_is_none_before_preparation(self, db, match_psg_lyon):
        """match_stats must be None until PreparationService runs."""
        fetched = db.query(FootballMatch).filter_by(id=match_psg_lyon.id).first()
        assert fetched.stats is None

    def test_filter_by_season(self, db, team_psg, team_lyon):
        db.add(FootballMatch(
            league_season=2023, home_team_id=team_psg.id,
            away_team_id=team_lyon.id, result="D",
            home_score=1, away_score=1, date="2023-03-01",
        ))
        db.add(FootballMatch(
            league_season=2024, home_team_id=team_lyon.id,
            away_team_id=team_psg.id, result="A",
            home_score=0, away_score=2, date="2024-02-01",
        ))
        db.flush()
        count_2024 = db.query(FootballMatch).filter_by(league_season=2024).count()
        assert count_2024 >= 1

    def test_fk_restrict_prevents_team_delete(self, db, match_psg_lyon, team_psg):
        """ondelete=RESTRICT — deleting a team with matches must raise."""
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            db.delete(team_psg)
            db.flush()
