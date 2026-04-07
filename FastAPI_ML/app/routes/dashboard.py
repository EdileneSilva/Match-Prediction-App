from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.match import Team
from ..utils.scraper_ligue1 import fetch_upcoming_matches, fetch_league_standings
from ..utils.team_mapper import normalize_team
import random

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def upsert_team(db: Session, team_name: str):
    """Crée l'équipe si elle n'existe pas."""
    team = db.query(Team).filter(Team.name == team_name).first()
    if not team:
        new_team = Team(name=team_name)
        db.add(new_team)
        db.commit()
    return team

@router.get("/upcoming")
def get_upcoming(db: Session = Depends(get_db)):
    """
    Récupère les prochains matchs de Ligue 1 via le scraper.
    """
    try:
        matches = fetch_upcoming_matches()
        
        for m in matches:
            # Simulation d'indice de confiance IA
            m["confidence_percent"] = random.randint(65, 89)
            m["is_derby"] = random.random() > 0.8
            
            # On normalise les noms pour le frontend/ML
            m["home"]["name"] = normalize_team(m["home"]["name"])
            m["away"]["name"] = normalize_team(m["away"]["name"])
            
            # Format expected by frontend: home_team, away_team
            m["home_team"] = m.pop("home")
            m["away_team"] = m.pop("away")
            
        return {
            "matches": matches,
            "round_name": "Prochaines Rencontres",
            "dates": "Ligue 1 McDonald's"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/standings")
def get_standings(db: Session = Depends(get_db)):
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
                "position": s.get("rank"),
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
