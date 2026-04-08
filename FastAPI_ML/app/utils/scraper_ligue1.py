import requests
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Entêtes pour simuler un navigateur et éviter le blocage
# L'API LFP nécessite certains headers spécifiques
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.4 Safari/605.1.15",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://ligue1.com",
    "Referer": "https://ligue1.com/",
    "application": "ligue1",
    "client-language": "fr-FR",
    "platform": "web"
}

def fetch_upcoming_matches(limit: int = 20):
    """
    Interroge l'API cachée de la LFP pour récupérer les prochains matchs officiels.
    """
    # On augmente le daysLimit pour avoir une vision sur toute la semaine / prochaine journée
    URL_MATCHES = "https://ma-api.ligue1.fr/championships-daily-calendars/matches?timezone=Europe/Paris&daysLimit=10&lookAfter=true"
    
    try:
        response = requests.get(URL_MATCHES, headers=headers, timeout=10.0)

        if response.status_code != 200:
            logger.error(f"Erreur API Ligue 1 : {response.status_code}")
            return []

        data = response.json()
        
        # Le format LFP pour cette route varie, si results est un dict de dates ou un tableau direct
        matches_dict = {}
        results = data.get("results", {})
        
        if isinstance(results, dict):
            # Si results est un dict, on cherche "matches" ou on itère sur les clés (dates)
            if "matches" in results:
                matches_dict = results["matches"]
            else:
                for date_key, date_data in results.items():
                    if isinstance(date_data, dict) and "matches" in date_data:
                        matches_dict.update(date_data["matches"])
        elif isinstance(results, list):
             for item in results:
                 if isinstance(item, dict) and "matches" in item:
                     matches_dict.update(item["matches"])

        if not matches_dict:
             return []

        all_matches = []
        for match_id, match in matches_dict.items():
            # Filtrer uniquement la Ligue 1 (ID championnat 1 ou "ligue1mcdonalds")
            championship_id = match.get("championshipId")
            if championship_id not in [1, 61, "1", "ligue1mcdonalds"]: 
                continue
                
            match_status = match.get("matchState", {}).get("name", "")
            if match_status in ["Finished", "Terminé", "Played"]:
                continue 

            try:
                home_team = match["home"]["clubIdentity"]["name"]
                away_team = match["away"]["clubIdentity"]["name"]

                home_logo = match["home"]["clubIdentity"]["assets"]["logo"]["medium"]
                away_logo = match["away"]["clubIdentity"]["assets"]["logo"]["medium"]

                date = match.get("date")
                gameweek = match.get("gameWeekNumber")

                all_matches.append({
                    "home": {"name": home_team, "logo": home_logo, "id": match["home"].get("id", 0)},
                    "away": {"name": away_team, "logo": away_logo, "id": match["away"].get("id", 0)},
                    "date": date,
                    "gameweek": gameweek,
                    "tag": f"Journée {gameweek}",
                    "is_derby": False
                })
            except (KeyError, TypeError) as e:
                logger.warning(f"Données manquantes dans la structure LFP : {e}")
                continue

        # Trier par date pour s'assurer de l'ordre chronologique
        all_matches.sort(key=lambda x: x['date'] if x['date'] else "")
        return all_matches[:limit]

    except Exception as e:
        logger.error(f"Erreur inattendue scraper LFP : {e}")
        return []

def fetch_league_standings():
    """
    Récupère le classement actuel du championnat de Ligue 1.
    """
    URL_STANDINGS = "https://ma-api.ligue1.fr/championship-standings/1/general"
    try:
        response = requests.get(URL_STANDINGS, headers=headers, timeout=10.0)
        if response.status_code != 200:
            logger.error(f"Erreur API Classement : {response.status_code}")
            return []
            
        data = response.json()
        standings_raw = data.get("standings", {})
        
        # On trie par rank (les clés sont des strings "1", "2"...)
        sorted_ranks = sorted(standings_raw.keys(), key=lambda x: int(x))
        
        results = []
        for rank_key in sorted_ranks:
            s = standings_raw[rank_key]
            club = s.get("clubIdentity", {})
            results.append({
                "rank": s.get("rank"),
                "team": club.get("name"),
                "logo": club.get("assets", {}).get("logo", {}).get("medium"),
                "played": s.get("played"),
                "points": s.get("points"),
                "wins": s.get("wins"),
                "draws": s.get("draws"),
                "losses": s.get("losses"),
                "goals_for": s.get("forGoals"),
                "goals_against": s.get("againstGoals"),
                "goals_diff": s.get("goalsDifference")
            })
        return results
    except Exception as e:
        logger.error(f"Erreur récupération classement : {e}")
        return []


def fetch_top_scorers(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Récupère les meilleurs buteurs joueurs (stat "goals") via l'API avancée LFP.
    """
    url = f"https://ma-api.ligue1.fr/championship-players-advanced-rankings/1/stat/goals?page=1&limit={limit}"
    try:
        response = requests.get(url, headers=headers, timeout=10.0)
        if response.status_code != 200:
            logger.error(f"Erreur API Buteurs joueurs : {response.status_code}")
            return []

        data = response.json()
        ranking = data.get("ranking", [])
        players_data = data.get("playersData", {})
        stats_indexes = data.get("statsIndexes", {})
        goals_idx = stats_indexes.get("goals")
        matches_idx = stats_indexes.get("matchesPlayed")

        results: List[Dict[str, Any]] = []
        for player_id in ranking[:limit]:
            player = players_data.get(str(player_id))
            if not player:
                continue
            identity = player.get("identity", {})
            stats = player.get("stats", [])
            if goals_idx is None or goals_idx >= len(stats):
                continue

            goals = int(stats[goals_idx] or 0)
            matches_played = int(stats[matches_idx] or 0) if isinstance(matches_idx, int) and matches_idx < len(stats) else 0
            first_name = (identity.get("firstName") or "").strip()
            last_name = (identity.get("lastName") or "").strip()
            full_name = f"{first_name} {last_name}".strip() or identity.get("displayName") or "Joueur inconnu"
            current_club_id = player.get("currentClubId")

            results.append({
                "id": str(player_id),
                "name": full_name,
                "team_id": current_club_id,
                "goals": goals,
                "matches": matches_played,
            })
        return results
    except Exception as e:
        logger.error(f"Erreur récupération buteurs joueurs : {e}")
        return []


def fetch_club_total_goals(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Récupère les buts marqués par équipe (stat "totalGoals") via l'API avancée LFP.
    """
    url = f"https://ma-api.ligue1.fr/championship-clubs-advanced-rankings/1/stat/totalGoals?page=1&limit={limit}"
    try:
        response = requests.get(url, headers=headers, timeout=10.0)
        if response.status_code != 200:
            logger.error(f"Erreur API Buts équipes : {response.status_code}")
            return []

        data = response.json()
        ranking = data.get("ranking", [])
        clubs_data = data.get("clubsData", {})
        stats_indexes = data.get("statsIndexes", {})
        total_goals_idx = stats_indexes.get("totalGoals")
        matches_idx = stats_indexes.get("matchesPlayed")

        results: List[Dict[str, Any]] = []
        for club_id in ranking[:limit]:
            club = clubs_data.get(club_id)
            if not club:
                continue
            identity = club.get("identity", {})
            stats = club.get("stats", [])
            if total_goals_idx is None or total_goals_idx >= len(stats):
                continue

            goals = int(stats[total_goals_idx] or 0)
            matches_played = int(stats[matches_idx] or 0) if isinstance(matches_idx, int) and matches_idx < len(stats) else 0
            logo = (((identity.get("assets") or {}).get("logo") or {}).get("medium"))
            results.append({
                "id": club_id,
                "team": identity.get("name") or "Équipe inconnue",
                "short_name": identity.get("shortName"),
                "logo": logo,
                "goals": goals,
                "matches_played": matches_played,
            })
        return results
    except Exception as e:
        logger.error(f"Erreur récupération buts équipes : {e}")
        return []

if __name__ == "__main__":
    import pprint
    print("--- MATCHS À VENIR ---")
    pprint.pprint(fetch_upcoming_matches(5))
    print("\n--- CLASSEMENT ---")
    pprint.pprint(fetch_league_standings()[:5])
