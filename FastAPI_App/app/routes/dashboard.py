from fastapi import APIRouter, HTTPException, Path
import httpx
import logging
import requests
from ..core.config import settings
from ..utils.team_mapper import normalize_team

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard Proxy"])

LFP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.4 Safari/605.1.15",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://ligue1.com",
    "Referer": "https://ligue1.com/",
    "application": "ligue1",
    "client-language": "fr-FR",
    "platform": "web",
}

@router.get("/upcoming")
async def proxy_upcoming():
    """
    Proxy vers l'API ML pour récupérer les prochains matchs.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/upcoming"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")

@router.get("/standings")
async def proxy_standings():
    """
    Proxy vers l'API ML pour récupérer le classement.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/standings"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")


@router.get("/goals-stats")
async def proxy_goals_stats():
    """
    Récupère les stats buts réelles (joueurs + équipes) directement via l'API LFP.
    """
    try:
        players_url = "https://ma-api.ligue1.fr/championship-players-advanced-rankings/1/stat/goals?page=1&limit=10"
        clubs_url = "https://ma-api.ligue1.fr/championship-clubs-advanced-rankings/1/stat/totalGoals?page=1&limit=20"

        players_res = requests.get(players_url, headers=LFP_HEADERS, timeout=12.0)
        clubs_res = requests.get(clubs_url, headers=LFP_HEADERS, timeout=12.0)
        players_res.raise_for_status()
        clubs_res.raise_for_status()

        players_raw = players_res.json()
        clubs_raw = clubs_res.json()

        players_ranking = players_raw.get("ranking", [])
        players_data = players_raw.get("playersData", {})
        players_indexes = players_raw.get("statsIndexes", {})
        player_goals_idx = players_indexes.get("goals")
        player_matches_idx = players_indexes.get("matchesPlayed")

        clubs_ranking = clubs_raw.get("ranking", [])
        clubs_data = clubs_raw.get("clubsData", {})
        clubs_indexes = clubs_raw.get("statsIndexes", {})
        club_goals_idx = clubs_indexes.get("totalGoals")
        club_matches_idx = clubs_indexes.get("matchesPlayed")

        clubs_list = []
        for club_id in clubs_ranking:
            club = clubs_data.get(club_id)
            if not club:
                continue
            identity = club.get("identity", {})
            stats = club.get("stats", [])
            if not isinstance(club_goals_idx, int) or club_goals_idx >= len(stats):
                continue
            goals = int(stats[club_goals_idx] or 0)
            matches_played = int(stats[club_matches_idx] or 0) if isinstance(club_matches_idx, int) and club_matches_idx < len(stats) else 0
            logo = (((identity.get("assets") or {}).get("logo") or {}).get("medium"))
            clubs_list.append({
                "id": club_id,
                "team": normalize_team(identity.get("name") or "Équipe inconnue"),
                "logo": logo,
                "goals": goals,
                "matches_played": matches_played,
            })

        clubs_by_id = {c["id"]: c for c in clubs_list}
        top_scorers = []
        for player_id in players_ranking[:10]:
            player = players_data.get(str(player_id))
            if not player:
                continue
            identity = player.get("identity", {})
            stats = player.get("stats", [])
            if not isinstance(player_goals_idx, int) or player_goals_idx >= len(stats):
                continue
            goals = int(stats[player_goals_idx] or 0)
            matches = int(stats[player_matches_idx] or 0) if isinstance(player_matches_idx, int) and player_matches_idx < len(stats) else 0
            club = clubs_by_id.get(player.get("currentClubId"))
            first_name = (identity.get("firstName") or "").strip()
            last_name = (identity.get("lastName") or "").strip()
            top_scorers.append({
                "id": str(player_id),
                "name": f"{first_name} {last_name}".strip() or "Joueur inconnu",
                "team": club["team"] if club else "N/A",
                "team_logo": club["logo"] if club else None,
                "goals": goals,
                "matches": matches,
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
    except requests.HTTPError as e:
        logger.error(f"Erreur HTTP LFP stats buts : {e}")
        raise HTTPException(status_code=502, detail="Erreur de récupération des stats LFP")
    except Exception as e:
        logger.error(f"Erreur goals-stats : {e}")
        raise HTTPException(status_code=500, detail="Service statistiques indisponible")
