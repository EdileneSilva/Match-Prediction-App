from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.match import Team
from ..utils.scraper_ligue1 import (
    fetch_upcoming_matches,
    fetch_league_standings,
    fetch_top_scorers,
    fetch_club_total_goals,
)
from ..utils.team_mapper import normalize_team
import random

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def upsert_team(db: Session, team_name: str, logo_url: str):
    """Met à jour le logo ou crée l'équipe si elle n'existe pas."""
    team = db.query(Team).filter(Team.name == team_name).first()
    if not team:
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


@router.get("/goals-stats")
def get_goals_stats():
    """
    Récupère les stats buts réelles (joueurs + équipes) depuis l'API LFP.
    """
    try:
        top_scorers = fetch_top_scorers(limit=10)
        clubs_goals = fetch_club_total_goals(limit=20)

        clubs_by_id = {club["id"]: club for club in clubs_goals}
        top_scorers_mapped = []
        for scorer in top_scorers:
            club = clubs_by_id.get(scorer.get("team_id"))
            top_scorers_mapped.append({
                **scorer,
                "team": normalize_team(club.get("team")) if club and club.get("team") else "N/A",
                "team_logo": club.get("logo") if club else None,
            })

        total_goals = sum(int(c.get("goals", 0)) for c in clubs_goals)
        total_matches = sum(int(c.get("matches_played", 0)) for c in clubs_goals)
        # Les matchs joués sont comptés pour chaque équipe, on divise donc par 2.
        league_matches = total_matches / 2 if total_matches > 0 else 0
        avg_goals_per_match = round(total_goals / league_matches, 2) if league_matches > 0 else 0

        clubs_distribution = sorted(
            [
                {
                    "id": c["id"],
                    "team": normalize_team(c["team"]),
                    "logo": c.get("logo"),
                    "goals": c.get("goals", 0),
                    "matches_played": c.get("matches_played", 0),
                    "percentage": round((int(c.get("goals", 0)) / total_goals) * 100, 1) if total_goals > 0 else 0,
                }
                for c in clubs_goals
            ],
            key=lambda x: x["goals"],
            reverse=True,
        )

        top_scorer = top_scorers_mapped[0] if top_scorers_mapped else {"name": "N/A", "goals": 0}

        return {
            "status": "success",
            "data": {
                "total_goals": total_goals,
                "avg_goals_per_match": avg_goals_per_match,
                "top_scorer": top_scorer,
                "top_scorers": top_scorers_mapped,
                "clubs_goals_distribution": clubs_distribution,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def register_dashboard_routes(app):
    app.include_router(router)
