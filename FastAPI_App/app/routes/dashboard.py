from fastapi import APIRouter, HTTPException
import logging
import random
from ..utils.team_mapper import normalize_team
from app.utils.scraper_ligue1 import (
    fetch_upcoming_matches,
    fetch_league_standings,
    fetch_top_scorers,
    fetch_club_total_goals,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["Dashboard Proxy"])

@router.get("/upcoming")
async def proxy_upcoming():
    """
    Récupère les prochains matchs de Ligue 1 via l'API LFP.
    """
    try:
        raw_matches = fetch_upcoming_matches(limit=20)
        matches = []
        for match in raw_matches:
            home = match.get("home", {})
            away = match.get("away", {})
            gameweek = match.get("gameweek")
            matches.append({
                "home_team": {"name": normalize_team(home.get("name", "")), "logo": home.get("logo"), "id": home.get("id", 0)},
                "away_team": {"name": normalize_team(away.get("name", "")), "logo": away.get("logo"), "id": away.get("id", 0)},
                "date": match.get("date"),
                "gameweek": gameweek,
                "tag": f"Journée {gameweek}",
                "confidence_percent": random.randint(65, 89),
                "is_derby": random.random() > 0.8,
            })

        return {
            "matches": matches[:20],
            "round_name": "Prochaines Rencontres",
            "dates": "Ligue 1 McDonald's",
        }
    except Exception as e:
        logger.error(f"Erreur upcoming : {e}")
        raise HTTPException(status_code=500, detail="Service dashboard indisponible")

@router.get("/standings")
async def proxy_standings():
    """
    Récupère le classement Ligue 1 via l'API LFP.
    """
    try:
        standings_raw = fetch_league_standings()
        standings = []
        for row in standings_raw:
            standings.append({
                "rank": row.get("rank"),
                "position": row.get("rank"),
                "team": normalize_team(row.get("team") or "N/A"),
                "logo": row.get("logo"),
                "played": row.get("played"),
                "points": row.get("points"),
                "wins": row.get("wins"),
                "draws": row.get("draws"),
                "losses": row.get("losses"),
                "goals_for": row.get("goals_for"),
                "goals_against": row.get("goals_against"),
                "goals_diff": row.get("goals_diff"),
                "form": row.get("form", []),
            })

        return {"status": "success", "data": standings}
    except Exception as e:
        logger.error(f"Erreur standings : {e}")
        raise HTTPException(status_code=500, detail="Service classement indisponible")


@router.get("/goals-stats")
async def proxy_goals_stats():
    """
    Récupère les stats buts réelles (joueurs + équipes) directement via l'API LFP.
    """
    try:
        clubs_list = [
            {**c, "team": normalize_team(c.get("team") or "Équipe inconnue")}
            for c in fetch_club_total_goals(limit=20)
        ]

        clubs_by_id = {c["id"]: c for c in clubs_list}
        top_scorers = []
        for scorer in fetch_top_scorers(limit=10):
            club = clubs_by_id.get(scorer.get("team_id"))
            top_scorers.append({
                "id": scorer.get("id"),
                "name": scorer.get("name"),
                "team": club["team"] if club else "N/A",
                "team_logo": club["logo"] if club else None,
                "goals": scorer.get("goals", 0),
                "matches": scorer.get("matches", 0),
            })

        total_goals = sum(c["goals"] for c in clubs_list)
        total_matches = sum(c["matches_played"] for c in clubs_list)
        league_matches = total_matches / 2 if total_matches > 0 else 0
        avg_goals_per_match = round(total_goals / league_matches, 2) if league_matches > 0 else 0

        clubs_distribution = sorted(
            [
                {
                    **c,
                    "percentage": round((c["goals"] / total_goals) * 100, 1) if total_goals > 0 else 0,
                }
                for c in clubs_list
            ],
            key=lambda x: x["goals"],
            reverse=True,
        )

        top_scorer = top_scorers[0] if top_scorers else {"name": "N/A", "goals": 0}

        return {
            "status": "success",
            "data": {
                "total_goals": total_goals,
                "avg_goals_per_match": avg_goals_per_match,
                "top_scorer": top_scorer,
                "top_scorers": top_scorers,
                "clubs_goals_distribution": clubs_distribution,
            },
        }
    except Exception as e:
        logger.error(f"Erreur goals-stats : {e}")
        raise HTTPException(status_code=500, detail="Service statistiques indisponible")
