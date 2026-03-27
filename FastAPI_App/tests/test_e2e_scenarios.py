import pytest
import respx
import httpx
from fastapi import status
from app.models.team import Team

@pytest.mark.asyncio
async def test_full_user_journey(client, db):
    # 1. Inscription d'un nouvel utilisateur
    user_payload = {
        "username": "journey_user",
        "email": "journey@test.com",
        "password": "SecurePass123"
    }
    resp_reg = client.post("/auth/register", json=user_payload)
    assert resp_reg.status_code == status.HTTP_201_CREATED
    
    # 2. Login pour obtenir le token
    resp_login = client.post("/auth/login", json={
        "email": user_payload["email"],
        "password": user_payload["password"]
    })
    assert resp_login.status_code == 200
    token = resp_login.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Préparation des données (Teams)
    team1 = Team(id=1, name="Paris Saint-Germain", short_name="PSG", logo_url="/static/logos/psg.svg")
    team2 = Team(id=2, name="Olympique de Marseille", short_name="OM", logo_url="/static/logos/om.svg")
    db.add(team1)
    db.add(team2)
    db.commit()
    
    # 4. Faire une prédiction (Mocking ML Service)
    async with respx.mock:
        respx.post("http://localhost:8001/predict").mock(return_value=httpx.Response(200, json={
            "prediction": "HOME_WIN",
            "confidence": 0.75
        }))
        
        predict_payload = {
            "home_team_id": 1,
            "away_team_id": 2,
            "referee": "Clément Turpin",
            "season": 2024,
            "round": 1
        }
        resp_pred = client.post("/predictions/predict", json=predict_payload, headers=auth_headers)
        assert resp_pred.status_code == 200
        assert resp_pred.json()["prediction"] == "HOME_WIN"
        
    # 5. Vérifier l'historique de l'utilisateur
    resp_hist = client.get("/predictions/history", headers=auth_headers)
    assert resp_hist.status_code == 200
    history = resp_hist.json()
    assert len(history) == 1
    assert history[0]["home_team_name"] == "Paris Saint-Germain"
    assert history[0]["prediction"] == "HOME_WIN"
    
    # 6. Vérifier les statistiques de l'utilisateur
    resp_stats = client.get("/auth/me/stats", headers=auth_headers)
    assert resp_stats.status_code == 200
    assert resp_stats.json()["total_predictions"] == 1
