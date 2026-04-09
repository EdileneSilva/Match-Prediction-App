import logging
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.4 Safari/605.1.15",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://ligue1.com",
    "Referer": "https://ligue1.com/",
    "application": "ligue1",
    "client-language": "fr-FR",
    "platform": "web",
}


def fetch_upcoming_matches(limit: int = 20) -> List[Dict[str, Any]]:
    url = "https://ma-api.ligue1.fr/championships-daily-calendars/matches?timezone=Europe/Paris&daysLimit=10&lookAfter=true"
    response = requests.get(url, headers=headers, timeout=12.0)
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results", {})

    matches_dict: Dict[str, Any] = {}
    if isinstance(results, dict):
        if isinstance(results.get("matches"), dict):
            matches_dict = results["matches"]
        else:
            for date_data in results.values():
                if isinstance(date_data, dict) and isinstance(date_data.get("matches"), dict):
                    matches_dict.update(date_data["matches"])
    elif isinstance(results, list):
        for item in results:
            if isinstance(item, dict) and isinstance(item.get("matches"), dict):
                matches_dict.update(item["matches"])

    all_matches: List[Dict[str, Any]] = []
    for match in matches_dict.values():
        if not isinstance(match, dict):
            continue
        championship_id = match.get("championshipId")
        if championship_id not in [1, 61, "1", "ligue1mcdonalds"]:
            continue

        match_status = ((match.get("matchState") or {}).get("name") or "").strip().lower()
        if match_status in ["finished", "termine", "terminé", "played"]:
            continue

        try:
            home = match["home"]["clubIdentity"]
            away = match["away"]["clubIdentity"]
            all_matches.append({
                "home": {"name": home["name"], "logo": ((home.get("assets") or {}).get("logo") or {}).get("medium"), "id": match["home"].get("id", 0)},
                "away": {"name": away["name"], "logo": ((away.get("assets") or {}).get("logo") or {}).get("medium"), "id": match["away"].get("id", 0)},
                "date": match.get("date"),
                "gameweek": match.get("gameWeekNumber"),
            })
        except Exception:
            continue

    all_matches.sort(key=lambda x: x["date"] or "")
    return all_matches[:limit]


def fetch_league_standings() -> List[Dict[str, Any]]:
    url = "https://ma-api.ligue1.fr/championship-standings/1/general"
    response = requests.get(url, headers=headers, timeout=12.0)
    response.raise_for_status()
    data = response.json()
    standings_raw = data.get("standings", {})

    # Conversão w/d/l → V/N/D
    result_map = {"w": "V", "d": "N", "l": "D"}

    sorted_ranks = sorted(standings_raw.keys(), key=lambda x: int(x))
    standings = []
    for rank_key in sorted_ranks:
        row = standings_raw[rank_key]
        club = row.get("clubIdentity", {})

        # Últimos 5 resultados a partir de seasonResults
        season_results = row.get("seasonResults") or []
        form = [
            result_map.get(r.get("resultLetter", "").lower(), "")
            for r in season_results[-5:]
        ]

        standings.append({
            "rank":          row.get("rank"),
            "team":          club.get("name"),
            "logo":          ((club.get("assets") or {}).get("logo") or {}).get("medium"),
            "played":        row.get("played"),
            "points":        row.get("points"),
            "wins":          row.get("wins"),
            "draws":         row.get("draws"),
            "losses":        row.get("losses"),
            "goals_for":     row.get("forGoals"),
            "goals_against": row.get("againstGoals"),
            "goals_diff":    row.get("goalsDifference"),
            "form":          form,  # ← ['V', 'V', 'D', 'V', 'V']
        })
    return standings


def fetch_top_scorers(limit: int = 10) -> List[Dict[str, Any]]:
    url = f"https://ma-api.ligue1.fr/championship-players-advanced-rankings/1/stat/goals?page=1&limit={limit}"
    response = requests.get(url, headers=headers, timeout=12.0)
    response.raise_for_status()
    data = response.json()

    ranking = data.get("ranking", [])
    players_data = data.get("playersData", {})
    stats_indexes = data.get("statsIndexes", {})
    goals_idx = stats_indexes.get("goals")
    matches_idx = stats_indexes.get("matchesPlayed")

    scorers = []
    for player_id in ranking[:limit]:
        player = players_data.get(str(player_id))
        if not player:
            continue
        identity = player.get("identity", {})
        stats = player.get("stats", [])
        if not isinstance(goals_idx, int) or goals_idx >= len(stats):
            continue

        first_name = (identity.get("firstName") or "").strip()
        last_name = (identity.get("lastName") or "").strip()
        scorers.append({
            "id": str(player_id),
            "name": f"{first_name} {last_name}".strip() or "Joueur inconnu",
            "team_id": player.get("currentClubId"),
            "goals": int(stats[goals_idx] or 0),
            "matches": int(stats[matches_idx] or 0) if isinstance(matches_idx, int) and matches_idx < len(stats) else 0,
        })
    return scorers


def fetch_club_total_goals(limit: int = 20) -> List[Dict[str, Any]]:
    url = f"https://ma-api.ligue1.fr/championship-clubs-advanced-rankings/1/stat/totalGoals?page=1&limit={limit}"
    response = requests.get(url, headers=headers, timeout=12.0)
    response.raise_for_status()
    data = response.json()

    ranking = data.get("ranking", [])
    clubs_data = data.get("clubsData", {})
    stats_indexes = data.get("statsIndexes", {})
    goals_idx = stats_indexes.get("totalGoals")
    matches_idx = stats_indexes.get("matchesPlayed")

    clubs = []
    for club_id in ranking[:limit]:
        club = clubs_data.get(club_id)
        if not club:
            continue
        identity = club.get("identity", {})
        stats = club.get("stats", [])
        if not isinstance(goals_idx, int) or goals_idx >= len(stats):
            continue
        clubs.append({
            "id": club_id,
            "team": identity.get("name") or "Équipe inconnue",
            "logo": ((identity.get("assets") or {}).get("logo") or {}).get("medium"),
            "goals": int(stats[goals_idx] or 0),
            "matches_played": int(stats[matches_idx] or 0) if isinstance(matches_idx, int) and matches_idx < len(stats) else 0,
        })
    return clubs
