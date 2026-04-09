import pytest
from unittest.mock import patch

def test_get_upcoming_matches(client):
    """Teste la route /dashboard/upcoming avec mocking du scraper."""
    mock_matches = [
        {
            "home": {"name": "Paris Saint-Germain", "logo": "psg.png", "id": 1},
            "away": {"name": "Olympique de Marseille", "logo": "om.png", "id": 2},
            "date": "2024-10-27T19:45:00Z",
            "gameweek": 9
        }
    ]
    
    with patch("app.routes.dashboard.fetch_upcoming_matches", return_value=mock_matches):
        response = client.get("/dashboard/upcoming")
        assert response.status_code == 200
        data = response.json()
        assert "matches" in data
        assert len(data["matches"]) == 1
        assert data["matches"][0]["home_team"]["name"] == "Paris SG"

def test_get_standings(client):
    """Teste la route /dashboard/standings avec mocking du scraper."""
    mock_standings = [
        {
            "rank": 1,
            "team": "Olympique de Marseille",
            "logo": "om.png",
            "played": 8,
            "points": 20,
            "wins": 6,
            "draws": 2,
            "losses": 0,
            "forGoals": 25,
            "againstGoals": 5,
            "goalsDifference": 20
        }
    ]
    
    with patch("app.routes.dashboard.fetch_league_standings", return_value=mock_standings):
        response = client.get("/dashboard/standings")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["team"] == "Marseille"

def test_get_goals_stats(client):
    """Teste la route /dashboard/goals-stats avec mocking du scraper."""
    mock_clubs = [
        {"id": "1", "team": "PSG", "logo": "psg.png", "goals": 10, "matches_played": 4}
    ]
    mock_scorers = [
        {"id": "100", "name": "Mbappé", "team_id": "1", "goals": 5, "matches": 4}
    ]
    
    with patch("app.routes.dashboard.fetch_club_total_goals", return_value=mock_clubs), \
         patch("app.routes.dashboard.fetch_top_scorers", return_value=mock_scorers):
        
        response = client.get("/dashboard/goals-stats")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["total_goals"] == 10
        assert data["data"]["top_scorer"]["name"] == "Mbappé"
