import pytest
import respx
import httpx
from app.models.team import Team
from app.core.config import settings

@respx.mock
def test_predict_success(client, auth_headers, db):
    """Teste la création d'une prédiction avec un mock de l'API ML."""
    
    # Mock de l'API ML externe (port 8001)
    ml_url = f"{settings.ML_API_URL}/predict"
    respx.post(ml_url).mock(return_value=httpx.Response(200, json={
        "prediction": "HOME_WIN",
        "confidence": 0.85,
        "probabilities": {"HOME": 0.85, "DRAW": 0.10, "AWAY": 0.05}
    }))

    payload = {
        "home_team": "psg",
        "away_team": "om",
        "season": "2024/2025"
    }
    
    response = client.post("/predictions/predict", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "HOME_WIN"
    assert data["confidence"] == 0.85
    assert data["home_team_logo_url"] == "psg.png"

def test_predict_team_not_found(client, auth_headers, db):
    """Teste l'erreur si une équipe n'existe pas en BDD."""
    payload = {
        "home_team": "inconnu",
        "away_team": "om",
        "season": "2024/2025"
    }
    response = client.post("/predictions/predict", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert "introuvables" in response.json()["detail"]

def test_get_prediction_history(client, auth_headers, db):
    """Teste la récupération de l'historique des prédictions (vide au début)."""
    response = client.get("/predictions/history", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0

def test_get_teams_list(client, db):
    """Teste la récupération de la liste des équipes."""
    response = client.get("/predictions/teams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(t["name"] == "psg" for t in data)
