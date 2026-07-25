from app.config import settings
from app.services.datasources.base import BaseDataSource


class Tank01Client(BaseDataSource):
    def __init__(self):
        super().__init__(
            base_url=f"https://{settings.tank01_host}",
            headers={
                "x-rapidapi-key": settings.tank01_key,
                "x-rapidapi-host": settings.tank01_host,
            },
        )

    def _check_key(self) -> None:
        if not settings.tank01_key:
            raise RuntimeError("Tank01-Key fehlt (ENV: TANK01_KEY)")

    def fetch_nfl_teams(self) -> list[dict]:
        self._check_key()
        resp = self._get("/getNFLTeams")
        body = resp.json().get("body", [])
        result = []
        for team in body:
            city = team.get("teamCity", "")
            name = team.get("teamName", "")
            full_name = f"{city} {name}".strip()
            external_raw = team.get("teamID")
            try:
                external_id = int(external_raw) if external_raw is not None else None
            except (ValueError, TypeError):
                external_id = None
            result.append({
                "name": full_name,
                "conference": team.get("conferenceAbv") or team.get("conference"),
                "division": team.get("division"),
                "abbreviation": team.get("teamAbv"),
                "city": city or None,
                "logo_url": team.get("teamLogo"),
                "external_id": external_id,
            })
        return result

    def fetch_games(
        self,
        game_week: int = 1,
        season: int = 2025,
        season_type: str = "reg",
    ) -> list[dict]:
        self._check_key()
        resp = self._get(
            "/getNFLGamesForWeek",
            params={"week": game_week, "seasonType": season_type, "season": season},
        )
        body = resp.json().get("body", [])
        result = []
        for game in body:
            result.append({
                "home_team": game.get("home"),
                "away_team": game.get("away"),
                "kickoff_time": game.get("gameTime") or game.get("gameDate"),
                "status": game.get("gameStatus"),
                "home_score": game.get("homePts"),
                "away_score": game.get("awayPts"),
                "external_id": game.get("gameID"),
                "season": season,
                "season_type": season_type,
                "week": game_week,
            })
        return result

    def fetch_standings(self, season: int) -> list[dict]:
        self._check_key()
        resp = self._get("/getNFLStandings", params={"season": season})
        body = resp.json().get("body", [])
        result = []
        for entry in body:
            division_rank_raw = entry.get("divisionRank")
            try:
                division_rank = int(division_rank_raw) if division_rank_raw is not None else None
            except (ValueError, TypeError):
                division_rank = None
            result.append({
                "team_abbreviation": entry.get("teamAbv"),
                "wins": int(entry.get("wins") or 0),
                "losses": int(entry.get("losses") or 0),
                "ties": int(entry.get("ties") or 0),
                "division_rank": division_rank,
            })
        return result
