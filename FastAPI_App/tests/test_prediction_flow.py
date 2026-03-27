import pytest
import respx
from httpx import Response
from app.models.team import Team

@pytest.mark.asyncio
async def test_predict_match_success(client, db, auth_headers):
    # 1. Préparation des équipes
    team1 = Team(name="Paris Saint-Germain", short_name="PSG", logo_url="/static/logos/psg.svg")
    team2 = Team(name="Olympique de Marseille", short_name="OM", logo_url="/static/logos/om.svg")
    db.add(team1)
    db.add(team2)
    db.commit()
    db.refresh(team1)
    db.refresh(team2)

    # 2. Mock de l'API ML avec respx
    with respx.mock:
        respx.post("http://localhost:8001/predict").mock(return_value=Response(
            200,
            json={"prediction": "HOME_WIN", "confidence": 0.85}
        ))

        # 3. Appel de l'API App (avec auth)
        payload = {
            "home_team_id": team1.id,
            "away_team_id": team2.id,
            "referee": "Clément Turpin",
            "season": 2024,
            "round": 25
        }

        response = client.post("/predictions/predict", json=payload, headers=auth_headers)

        # 4. Vérifications
        assert response.status_code == 200
        data = response.json()
        assert data["prediction"] == "HOME_WIN"
        assert data["confidence"] == 0.85

@pytest.mark.asyncio
async def test_predict_match_no_auth(client, db):
    """Vérifie qu'une requête sans token est refusée avec 401."""
    payload = {
        "home_team_id": 1,
        "away_team_id": 2,
        "season": 2024,
        "round": 1
    }
    response = client.post("/predictions/predict", json=payload)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_predict_match_team_not_found(client, db, auth_headers):
    # Appel avec IDs inexistants
    payload = {
        "home_team_id": 999,
        "away_team_id": 888
    }
    response = client.post("/predictions/predict", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert "introuvables" in response.json()["detail"]

@pytest.mark.asyncio
async def test_predict_match_ml_service_error(client, db, auth_headers):
    # 1. Préparation des données
    team = Team(name="Lens", short_name="RCL", logo_url="")
    db.add(team)
    db.commit()
    db.refresh(team)

    # 2. Mock d'une erreur 500 du service ML
    with respx.mock:
        respx.post("http://localhost:8001/predict").mock(return_value=Response(500))

        payload = {
            "home_team_id": team.id,
            "away_team_id": team.id
        }
        response = client.post("/predictions/predict", json=payload, headers=auth_headers)
        assert response.status_code == 503
        assert "Erreur de communication" in response.json()["detail"]
