from fastapi import APIRouter
from typing import List, Dict, Any
from ..utils.scraper_ligue1 import fetch_upcoming_matches, fetch_league_standings
import httpx
from ..core.config import settings

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Configuration URL du service ML
ML_SERVICE_URL = "http://localhost:8001"

from ..utils.team_mapper import normalize_team

async def get_prediction_confidence(home_team: str, away_team: str) -> Dict[str, Any]:
    """
    Interroge le service ML pour obtenir le taux de confiance réel.
    Désormais avec mapping des noms d'équipes pour éviter les erreurs.
    """
    # Mapper les noms LFP vers noms de modèle
    norm_home = normalize_team(home_team)
    norm_away = normalize_team(away_team)
    
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            payload = {
                "home_team": norm_home,
                "away_team": norm_away,
                "referee": "Unknown",
                "season": 2024, # Saison de référence dans le modèle
                "round": 1
            }
            # Appel à l'endpoint de FastAPI_ML
            response = await client.post(f"{ML_SERVICE_URL}/predict", json=payload)
            if response.status_code == 200:
                data = response.json()
                return {
                    "prediction": data.get("prediction", "DRAW"),
                    "confidence": round(data.get("confidence", 0.50) * 100)
                }
    except Exception as e:
         # Log simple sans bruit
         pass
        
    # Fallback honnête en cas d'erreur de service ou équipe inconnue
    return {
        "prediction": "N/A",
        "confidence": 50 # Valeur neutre si l'IA ne peut pas répondre
    }

@router.get("/upcoming")
async def get_upcoming_dashboard():
    """
    Renvoie les prochains matchs de Ligue 1 (scrappés de l'API LFP) avec leur 
    probabilité de prédiction IA.
    """
    # Récupérer les matchs réels (on passe une limite plus large pour avoir toute la journée)
    matches = fetch_upcoming_matches(limit=15)
    
    # Enrichir chaque match avec le pré-calcul de l'IA
    results = []
    for m in matches:
        ml_data = await get_prediction_confidence(m["home"]["name"], m["away"]["name"])
        results.append({
            "fixture_id": m["home"]["id"] + m["away"]["id"] if m["home"]["id"] else 0,
            "home_team": m["home"],
            "away_team": m["away"],
            "tag": m["tag"],
            "is_derby": m.get("is_derby", False),
            "ml_prediction": ml_data["prediction"],
            "confidence_percent": ml_data["confidence"]
        })
        
    return {
        "round_name": "Prochaines Rencontres - Ligue 1",
        "dates": "Saison 2025/2026",
        "matches": results
    }

@router.get("/standings")
async def get_standings_dashboard():
    """
    Renvoie le classement actuel du championnat.
    """
    standings = fetch_league_standings()
    return {
        "status": "success",
        "data": standings
    }
