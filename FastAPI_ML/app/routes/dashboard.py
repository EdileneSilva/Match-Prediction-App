from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.match import Team
from ..utils.scraper_ligue1 import fetch_upcoming_matches, fetch_league_standings
from ..utils.team_mapper import normalize_team
import random

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def upsert_team(db: Session, team_name: str, logo_url: str):
    """Met à jour le logo ou crée l'équipe si elle n'existe pas."""
    team = db.query(Team).filter(Team.name == team_name).first()
    if team:
        if logo_url and team.logo_url != logo_url:
            team.logo_url = logo_url
            db.commit()
    else:
        new_team = Team(name=team_name, logo_url=logo_url)
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
            home = m.get("home", {})
            away = m.get("away", {})
            
            # Upsert les équipes pour avoir les logos en base
            upsert_team(db, home.get("name"), home.get("logo"))
            upsert_team(db, away.get("name"), away.get("logo"))
            
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
    Récupère le classement actuel de Ligue 1 via le StatsService (API LFP).
    """
    from ..services.stats_service import stats_service
    try:
        standings = stats_service.fetch_full_standings()
        
        # Sync les logos et normalisation
        for s in standings:
            upsert_team(db, s["team"], s.get("logo"))
            s["team"] = normalize_team(s["team"])
            
        return {
            "status": "success",
            "data": standings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/squad-news")
def get_squad_news():
    """
    Récupère les blessures et suspensions actuelles.
    """
    from ..services.stats_service import stats_service
    try:
        news = stats_service.fetch_squad_news()
        return {
            "status": "success",
            "data": news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/league-stats/players/{stat_name}")
def get_players_stats(stat_name: str = "goals", limit: int = 10):
    """
    Récupère le classement des joueurs pour une statistique donnée.
    """
    from ..services.stats_service import stats_service
    return {
        "status": "success",
        "data": stats_service.fetch_player_stats(stat_name, limit)
    }

@router.get("/league-stats/clubs/{stat_name}")
def get_clubs_stats(stat_name: str = "totalGoals", limit: int = 10):
    """
    Récupère le classement des clubs pour une statistique donnée.
    """
    from ..services.stats_service import stats_service
    return {
        "status": "success",
        "data": stats_service.fetch_club_stats(stat_name, limit)
    }

@router.get("/league-stats/overview")
def get_stats_overview():
    """
    Récupère une vue d'ensemble des statistiques Ligue 1.
    """
    from ..services.stats_service import stats_service
    return {
        "status": "success",
        "data": stats_service.fetch_stats_overview()
    }

def register_dashboard_routes(app):
    app.include_router(router)
