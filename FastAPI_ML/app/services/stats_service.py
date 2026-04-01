import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

LFP_API_BASE = "https://ma-api.ligue1.fr"

class StatsService:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://ligue1.com",
            "Referer": "https://ligue1.com/",
            "application": "ligue1",
            "client-language": "fr-FR",
            "platform": "web"
        }

    def _get_api_data(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        try:
            url = f"{LFP_API_BASE}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params or {}, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erreur API LFP ({endpoint}): {e}")
            return None

    def fetch_current_game_week(self) -> int:
        """Récupère le numéro de la journée actuelle."""
        data = self._get_api_data("championship-matches/championship/1/current")
        if data and "gameWeekNumber" in data:
            return data["gameWeekNumber"]
        return 27 # Valeur par défaut si échec

    def fetch_full_standings(self) -> List[Dict[str, Any]]:
        """Récupère le classement complet avec victoires, nuls, défaites et forme."""
        data = self._get_api_data("championship-standings/1/general", {"season": 2025})
        if not data or "standings" not in data:
            return []

        results = []
        for team in data["standings"].values(): # C'est un dictionnaire indexé par rang
            identity = team.get("clubIdentity", {})
            
            # Forme : 'w', 'd', 'l' -> 'V', 'N', 'D'
            form_history = []
            for res in team.get("seasonResults", [])[-10:]: # 10 derniers matchs (plus pour calculs)
                letter = res.get("resultLetter", "").upper()
                if letter == "W": form_history.append("V")
                elif letter == "D": form_history.append("N")
                elif letter == "L": form_history.append("D")
            
            results.append({
                "id": identity.get("id"), # l1_championship_club_2025_XX
                "position": team.get("rank"),
                "team": identity.get("name"),
                "logo": identity.get("assets", {}).get("logo", {}).get("medium"),
                "played": team.get("played"),
                "wins": team.get("wins"),
                "draws": team.get("draws"),
                "losses": team.get("losses"),
                "goals_for": team.get("forGoals"),
                "goals_against": team.get("againstGoals"),
                "no_goal_conceded": team.get("noGoalConceded"), # Clean sheets
                "goals_diff": team.get("goalsDifference"),
                "points": team.get("points"),
                "form": form_history
            })
        return results

    def fetch_squad_news(self) -> Dict[str, List[Dict[str, Any]]]:
        """Récupère les blessures et suspensions en parsant la hiérarchie Matches."""
        gw = self.fetch_current_game_week()
        data = self._get_api_data(f"championship-players-statuses/1/game-week/{gw}")
        if not data or "playersStatuses" not in data:
            return {}

        matches = data["playersStatuses"].get("championshipMatches", {})
        players_data = data.get("playersData", {})
        
        news_by_club = {}
        
        status_map = {
            1: {"label": "Incertain", "color": "white", "emoji": "⚪"},
            2: {"label": "Blessé", "color": "red", "emoji": "🔴"},
            3: {"label": "Suspendu", "color": "yellow", "emoji": "🟡"},
            7: {"label": "Retour", "color": "green", "emoji": "🟢"}
        }

        for match in matches.values():
            for side in ["home", "away"]:
                club_id = match[side].get("clubId")
                if not club_id: continue
                
                if club_id not in news_by_club:
                    news_by_club[club_id] = []
                
                for p_status in match[side].get("playersStatuses", []):
                    status_id = p_status.get("status")
                    if status_id not in status_map: continue
                    
                    p_id = p_status.get("playerId")
                    # On tente de récupérer les infos même si p_id est un entier ou string
                    player_info = players_data.get(str(p_id)) or players_data.get(p_id) or {}
                    identity = player_info.get("identity", {})
                    
                    first_name = identity.get('firstName', '')
                    last_name = identity.get('lastName', '')
                    full_name = f"{first_name} {last_name}".strip()

                    reason_dict = p_status.get("reason") or {}
                    reason = reason_dict.get("fr-FR") or "Non spécifié"

                    news_by_club[club_id].append({
                        "player_id": p_id,
                        "name": full_name or "Joueur inconnu",
                        "status": status_map[status_id]["label"],
                        "color": status_map[status_id]["color"],
                        "emoji": status_map[status_id]["emoji"],
                        "reason": reason
                    })
        return news_by_club
    def fetch_player_stats(self, stat_name: str = "goals", limit: int = 10) -> List[Dict[str, Any]]:
        """Classement des joueurs."""
        data = self._get_api_data(f"championship-players-advanced-rankings/1/stat/{stat_name}", {"page": 1, "limit": limit})
        if not data: return []

        rank_ids = data.get("ranking", [])
        players_data = data.get("playersData", {})
        stats_indexes = data.get("statsIndexes", {})
        stat_index = stats_indexes.get(stat_name)
        
        if stat_index is None: return []

        results = []
        for i, p_id in enumerate(rank_ids):
            player_info = players_data.get(p_id, {})
            identity = player_info.get("identity", {})
            stats_array = player_info.get("stats", [])
            stat_value = stats_array[stat_index] if len(stats_array) > stat_index else 0
            
            results.append({
                "rank": i + 1,
                "player_id": p_id,
                "name": f"{identity.get('firstName', '')} {identity.get('lastName', '')}".strip(),
                "team": player_info.get("clubIdentity", {}).get("name") or "Ligue 1",
                "team_logo": player_info.get("clubIdentity", {}).get("assets", {}).get("logo", {}).get("medium"),
                "photo": identity.get("assets", {}).get("bustPictures", {}).get("medium"),
                "value": stat_value
            })
        return results

    def fetch_club_stats(self, stat_name: str = "totalGoals", limit: int = 10) -> List[Dict[str, Any]]:
        """Classement des clubs pour une stat."""
        data = self._get_api_data(f"championship-clubs-advanced-rankings/1/stat/{stat_name}", {"page": 1, "limit": limit})
        if not data: return []

        rank_ids = data.get("ranking", [])
        clubs_data = data.get("clubsData", {})
        stats_indexes = data.get("statsIndexes", {})
        stat_index = stats_indexes.get(stat_name)

        results = []
        for i, c_id in enumerate(rank_ids):
            club_info = clubs_data.get(c_id, {})
            identity = club_info.get("identity", {})
            stats_array = club_info.get("stats", [])
            stat_value = stats_array[stat_index] if stat_index is not None and len(stats_array) > stat_index else 0
            
            results.append({
                "rank": i + 1,
                "team": identity.get("name"),
                "logo": identity.get("assets", {}).get("logo", {}).get("medium"),
                "value": stat_value
            })
        return results

    def fetch_stats_overview(self) -> Dict[str, Any]:
        """Vue d'ensemble rapide."""
        standings = self.fetch_full_standings()
        if not standings: return {}
        
        best_attack = max(standings, key=lambda x: x["goals_for"])
        best_defense = min(standings, key=lambda x: x["goals_against"])
        
        return {
            "total_matches": sum(t["played"] for t in standings) // 2,
            "total_goals": sum(t["goals_for"] for t in standings),
            "best_attack": {"team": best_attack["team"], "value": best_attack["goals_for"]},
            "best_defense": {"team": best_defense["team"], "value": best_defense["goals_against"]}
        }

stats_service = StatsService()
