import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ml-api"}

@pytest.mark.asyncio
async def test_predict_success(client):
    payload = {
        "home_team": "Paris Saint-Germain",
        "away_team": "Olympique de Marseille",
        "referee": "Clément Turpin",
        "season": 2023,
        "round": 25
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert data["prediction"] in ["HOME_WIN", "AWAY_WIN", "DRAW"]
    assert 0 <= data["confidence"] <= 1

@pytest.mark.asyncio
async def test_predict_missing_fields(client):
    payload = {
        "home_team": "PSG"
        # Manque away_team
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
