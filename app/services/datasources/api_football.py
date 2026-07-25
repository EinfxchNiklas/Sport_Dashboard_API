from app.config import settings
from app.services.datasources.base import BaseDataSource


class ApiFootballClient(BaseDataSource):
    def __init__(self):
        super().__init__(
            base_url=settings.api_football_base_url,
            headers={"x-apisports-key": settings.api_football_key},
        )

    def _check_key(self) -> None:
        if not settings.api_football_key:
            raise RuntimeError("API-Football-Key fehlt (ENV: API_FOOTBALL_KEY)")

    def fetch_competition(self, league_id: int, season: int) -> dict | None:
        self._check_key()
        resp = self._get("/leagues", params={"id": league_id, "season": season})
        data = resp.json().get("response", [])
        if not data:
            return None
        entry = data[0]
        league = entry.get("league", {})
        country = entry.get("country", {})
        return {
            "name": league.get("name"),
            "sport": "football",
            "country": country.get("name"),
            "season": str(season),
            "logo_url": league.get("logo"),
            "external_id": league.get("id"),
        }

    def fetch_teams(self, league_id: int, season: int) -> list[dict]:
        self._check_key()
        resp = self._get("/teams", params={"league": league_id, "season": season})
        data = resp.json().get("response", [])
        result = []
        for entry in data:
            team = entry.get("team", {})
            result.append({
                "name": team.get("name"),
                "short_name": team.get("code"),
                "country": team.get("country"),
                "logo_url": team.get("logo"),
                "external_id": team.get("id"),
            })
        return result

    def fetch_matches(self, league_id: int, season: int) -> list[dict]:
        self._check_key()
        resp = self._get("/fixtures", params={"league": league_id, "season": season})
        data = resp.json().get("response", [])
        result = []
        for entry in data:
            fixture = entry.get("fixture", {})
            teams = entry.get("teams", {})
            goals = entry.get("goals", {})
            status = fixture.get("status", {})
            league_info = entry.get("league", {})
            round_str: str | None = league_info.get("round")
            # Spieltag aus "Regular Season - 5" o. Ä. extrahieren
            matchday: int | None = None
            group_name: str | None = None
            if round_str:
                parts = round_str.split(" - ")
                if len(parts) == 2:
                    try:
                        matchday = int(parts[1])
                    except ValueError:
                        group_name = parts[1].strip() if parts[1].strip() else None
            result.append({
                "home_team": teams.get("home", {}).get("name"),
                "away_team": teams.get("away", {}).get("name"),
                "kickoff_time": fixture.get("date"),
                "status": status.get("short"),
                "home_score": goals.get("home"),
                "away_score": goals.get("away"),
                "stage": status.get("long") or round_str,
                "matchday": matchday,
                "group_name": group_name,
                "external_id": fixture.get("id"),
            })
        return result

    def fetch_standings(self, league_id: int, season: int) -> list[dict]:
        self._check_key()
        resp = self._get("/standings", params={"league": league_id, "season": season})
        data = resp.json().get("response", [])
        result = []
        if not data:
            return result
        # standings ist eine Liste von Gruppen (bei Ligatabellen genau eine)
        standings_groups = data[0].get("league", {}).get("standings", [])
        for group in standings_groups:
            for entry in group:
                all_stats = entry.get("all", {})
                result.append({
                    "team_name": entry.get("team", {}).get("name"),
                    "group": entry.get("group"),
                    "rank": entry.get("rank"),
                    "played": all_stats.get("played", 0),
                    "won": all_stats.get("win", 0),
                    "draw": all_stats.get("draw", 0),
                    "lost": all_stats.get("lose", 0),
                    "goals_for": (all_stats.get("goals") or {}).get("for", 0),
                    "goals_against": (all_stats.get("goals") or {}).get("against", 0),
                    "goal_difference": entry.get("goalsDiff", 0),
                    "points": entry.get("points", 0),
                })
        return result

    def fetch_injuries(self, league_id: int, season: int) -> list[dict]:
        self._check_key()
        resp = self._get("/injuries", params={"league": league_id, "season": season})
        data = resp.json().get("response", [])
        result = []
        for entry in data:
            player = entry.get("player", {})
            team = entry.get("team", {})
            result.append({
                "player_name": player.get("name"),
                "team_name": team.get("name"),
                "position": player.get("position"),
                "age": player.get("age"),
                "description": player.get("reason") or player.get("type"),
                "status": player.get("type"),
                "player_external_id": player.get("id"),
            })
        return result
