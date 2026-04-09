"""
Integration tests — Team model (PostgreSQL)
"""
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.match import Team

pytestmark = pytest.mark.integration


class TestTeamModel:

    def test_insert_team(self, db):
        team = Team(name="Marseille")
        db.add(team)
        db.flush()
        assert team.id is not None

    def test_team_id_is_integer(self, db):
        team = Team(name="Monaco")
        db.add(team)
        db.flush()
        assert isinstance(team.id, int)

    def test_team_name_persisted(self, db):
        team = Team(name="Lens")
        db.add(team)
        db.flush()
        fetched = db.query(Team).filter_by(id=team.id).first()
        assert fetched.name == "Lens"

    def test_query_by_name(self, db):
        db.add(Team(name="Nice"))
        db.flush()
        result = db.query(Team).filter(Team.name == "Nice").first()
        assert result is not None
        assert result.name == "Nice"

    def test_multiple_teams_inserted(self, db):
        names = ["Toulouse", "Rennes", "Strasbourg"]
        for name in names:
            db.add(Team(name=name))
        db.flush()
        count = db.query(Team).filter(Team.name.in_(names)).count()
        assert count == 3

    def test_no_duplicate_check_by_default(self, db):
        """PostgreSQL does not enforce uniqueness on name unless constrained."""
        db.add(Team(name="Lyon"))
        db.add(Team(name="Lyon"))
        db.flush()
        count = db.query(Team).filter_by(name="Lyon").count()
        assert count == 2

    def test_team_has_empty_home_matches_by_default(self, db):
        team = Team(name="Brest")
        db.add(team)
        db.flush()
        assert team.home_matches == []

    def test_team_has_empty_away_matches_by_default(self, db):
        team = Team(name="Auxerre")
        db.add(team)
        db.flush()
        assert team.away_matches == []
