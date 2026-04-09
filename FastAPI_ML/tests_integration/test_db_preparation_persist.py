"""
Integration tests — PreparationService database operations (PostgreSQL)

These tests verify _seed_teams() and _persist() against a real Postgres instance,
which SQLite cannot replicate (FK RESTRICT, unique constraints, Float precision).
"""
import pytest
import pandas as pd
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.preparation import PreparationService
from app.models.match import Team, FootballMatch, MatchStats

pytestmark = pytest.mark.integration


@pytest.fixture
def svc():
    return PreparationService()


@pytest.fixture
def stats_df():
    """Minimal DataFrame that matches the output of _add_rolling_features()."""
    return pd.DataFrame({
        "Date":      pd.to_datetime(["2024-01-10", "2024-01-17", "2024-01-24"]),
        "HomeTeam":  ["Paris SG", "Lyon",    "Marseille"],
        "AwayTeam":  ["Lyon",     "Marseille", "Paris SG"],
        "HomeScore": [3, 1, 0],
        "AwayScore": [1, 1, 2],
        "Result":    ["H", "D", "A"],
        "HalftimeHomeGoals": [1, 0, 0],
        "HalftimeAwayGoals": [0, 0, 1],
        "HalftimeResult":    ["H", "D", "A"],
        "HomeShot":          [14, 8, 5],
        "AwayShot":          [6, 9, 12],
        "HomeShotTarget":    [6, 3, 2],
        "AwayShotTarget":    [2, 4, 5],
        "HomeTeamFouls":     [10, 12, 14],
        "AwayTeamFouls":     [11, 9, 8],
        "HomeTeamCorners":   [7, 4, 2],
        "AwayTeamCorners":   [3, 5, 7],
        "HomeYellowCards":   [1, 1, 3],
        "AwayYellowCards":   [2, 2, 0],
        "HomeRedCards":      [0, 0, 0],
        "AwayRedCards":      [0, 0, 0],
        "league.season":     [2024, 2024, 2024],
        "home_goals_scored_home":   [2.5, 1.5, 1.0],
        "home_goals_conceded_home": [0.8, 1.2, 1.5],
        "home_win_rate_home":       [0.75, 0.4, 0.3],
        "away_goals_scored_away":   [1.8, 1.2, 0.8],
        "away_goals_conceded_away": [1.0, 1.5, 1.8],
        "away_win_rate_away":       [0.55, 0.3, 0.2],
        "home_season_rank":         [1, 5, 8],
        "away_season_rank":         [5, 8, 1],
        "home_rolling_scored":      [0.0, 2.2, 1.4],
        "home_rolling_conceded":    [0.0, 0.6, 1.0],
        "home_rolling_win_rate":    [0.0, 0.8, 0.4],
        "away_rolling_scored":      [0.0, 1.6, 1.1],
        "away_rolling_conceded":    [0.0, 0.9, 1.4],
        "away_rolling_win_rate":    [0.0, 0.6, 0.2],
    })


# ---------------------------------------------------------------------------
# _seed_teams
# ---------------------------------------------------------------------------

class TestSeedTeamsPostgres:

    def test_inserts_all_unique_teams(self, svc, db, stats_df):
        svc._seed_teams(stats_df, db)
        team_names = {t.name for t in db.query(Team).all()}
        assert {"Paris SG", "Lyon", "Marseille"} <= team_names

    def test_does_not_insert_duplicates(self, svc, db, stats_df):
        svc._seed_teams(stats_df, db)
        svc._seed_teams(stats_df, db)  # second call
        count = db.query(Team).filter(
            Team.name.in_(["Paris SG", "Lyon", "Marseille"])).count()
        assert count == 3

    def test_existing_teams_not_duplicated(self, svc, db, stats_df):
        db.add(Team(name="Paris SG"))
        db.flush()
        svc._seed_teams(stats_df, db)
        count = db.query(Team).filter_by(name="Paris SG").count()
        assert count == 1


# ---------------------------------------------------------------------------
# _persist
# ---------------------------------------------------------------------------

class TestPersistPostgres:

    def test_inserts_correct_number_of_matches(self, svc, db, stats_df):
        inserted = svc._persist(stats_df, db)
        assert inserted == len(stats_df)

    def test_match_results_stored_correctly(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        results = {m.result for m in db.query(FootballMatch).all()}
        assert results == {"H", "D", "A"}

    def test_match_scores_stored_correctly(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        first = db.query(FootballMatch).order_by(FootballMatch.date).first()
        assert first.home_score == 3
        assert first.away_score == 1

    def test_match_stats_created_for_each_match(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        n_matches = db.query(FootballMatch).count()
        n_stats   = db.query(MatchStats).count()
        assert n_matches == n_stats

    def test_rolling_features_stored_correctly(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        first_stats = db.query(MatchStats).join(FootballMatch).order_by(
            FootballMatch.date).first()
        assert first_stats.home_rolling_scored   == 0.0
        assert first_stats.home_rolling_win_rate == 0.0

    def test_skips_duplicate_matches(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        inserted_second = svc._persist(stats_df, db)
        assert inserted_second == 0

    def test_total_match_count_after_duplicate(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        svc._persist(stats_df, db)
        total = db.query(FootballMatch).count()
        assert total == len(stats_df)

    def test_fk_restrict_on_team_with_matches(self, svc, db, stats_df):
        """PostgreSQL must raise IntegrityError on team delete with matches (RESTRICT)."""
        from sqlalchemy.exc import IntegrityError
        svc._persist(stats_df, db)
        psg = db.query(Team).filter_by(name="Paris SG").first()
        with pytest.raises(IntegrityError):
            db.delete(psg)
            db.flush()

    def test_cascade_delete_stats_with_match(self, svc, db, stats_df):
        """Deleting a FootballMatch must cascade-delete its MatchStats (ondelete=CASCADE).
        Uses raw SQL to bypass the ORM and let Postgres execute the CASCADE directly."""
        from sqlalchemy import text
        svc._persist(stats_df, db)
        match    = db.query(FootballMatch).first()
        stats_id = match.stats.id
        match_id = match.id
        db.execute(text("DELETE FROM football_matches WHERE id = :id"), {"id": match_id})
        db.flush()
        remaining = db.query(MatchStats).filter_by(id=stats_id).first()
        assert remaining is None

    def test_home_season_rank_stored_as_integer(self, svc, db, stats_df):
        svc._persist(stats_df, db)
        stats = db.query(MatchStats).first()
        assert stats.home_season_rank in [1, 5, 8]
