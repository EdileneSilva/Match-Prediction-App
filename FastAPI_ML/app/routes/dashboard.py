from fastapi import APIRouter, HTTPException
from ..utils.scraper_ligue1 import fetch_upcoming_matches, fetch_league_standings
from ..utils.team_mapper import normalize_team

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/upcoming")
def get_upcoming():
    """
    Récupère les prochains matchs de Ligue 1 via le scraper.
    """
    try:
        matches = fetch_upcoming_matches(limit=10)
        
        # On normalise les noms pour le frontend/ML
        for m in matches:
            m["home"]["name"] = normalize_team(m["home"]["name"])
            m["away"]["name"] = normalize_team(m["away"]["name"])
            
        return {
            "status": "success",
            "matches": matches,
            "round_name": "Prochaine Journée",
            "dates": "Ligue 1 McDonald's 2025-2026"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/standings")
def get_standings():
    """
    Récupère le classement actuel de Ligue 1 via le scraper.
    """
    try:
        standings = fetch_league_standings()
        
        # Normalisation et mapping pour le frontend
        standings_mapped = []
        for s in standings:
            standings_mapped.append({
                **s,
                "rank": s["position"],
                "team": normalize_team(s["team"])
            })
            
        return {
            "status": "success",
            "data": standings_mapped
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def register_dashboard_routes(app):
    app.include_router(router)
