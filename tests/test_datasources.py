import pytest
import respx
from httpx import Response

import app.config as config_module
from app.services.datasources import OpenF1Client, ApiFootballClient, Tank01Client


# ---------------------------------------------------------------------------
# OpenF1
# ---------------------------------------------------------------------------

@respx.mock
def test_openf1_fetch_races():
    respx.get("https://api.openf1.org/v1/meetings").mock(
        return_value=Response(
            200,
            json=[
                {
                    "meeting_official_name": "Bahrain Grand Prix",
                    "meeting_name": "Bahrain",
                    "date_start": "2025-03-02T15:00:00+00:00",
                }
            ],
        )
    )
    client = OpenF1Client()
    races = client.fetch_races(2025)
    assert len(races) == 1
    race = races[0]
    assert race["season"] == "2025"
    assert race["name"] == "Bahrain Grand Prix"
    assert race["date"] == "2025-03-02T15:00:00+00:00"
    assert race["status"] == "scheduled"


@respx.mock
def test_openf1_fetch_drivers_deduplication():
    respx.get("https://api.openf1.org/v1/drivers").mock(
        return_value=Response(
            200,
            json=[
                {"driver_number": 1, "full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
                {"driver_number": 1, "full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
                {"driver_number": 44, "full_name": "Lewis Hamilton", "team_name": "Ferrari"},
            ],
        )
    )
    client = OpenF1Client()
    drivers = client.fetch_drivers("latest")
    assert len(drivers) == 2
    assert drivers[0] == {"name": "Max Verstappen", "team": "Red Bull Racing", "number": 1, "abbreviation": None, "country": None, "team_color": None, "external_id": 1}
    assert drivers[1] == {"name": "Lewis Hamilton", "team": "Ferrari", "number": 44, "abbreviation": None, "country": None, "team_color": None, "external_id": 44}


@respx.mock
def test_openf1_fetch_drivers_fallback_name():
    respx.get("https://api.openf1.org/v1/drivers").mock(
        return_value=Response(
            200,
            json=[
                {
                    "driver_number": 16,
                    "first_name": "Charles",
                    "last_name": "Leclerc",
                    "team_name": "Ferrari",
                },
            ],
        )
    )
    client = OpenF1Client()
    drivers = client.fetch_drivers()
    assert drivers[0]["name"] == "Charles Leclerc"


# ---------------------------------------------------------------------------
# ApiFootball
# ---------------------------------------------------------------------------

@respx.mock
def test_api_football_fetch_competition(monkeypatch):
    monkeypatch.setattr(config_module.settings, "api_football_key", "test-key")
    respx.get("https://v3.football.api-sports.io/leagues").mock(
        return_value=Response(
            200,
            json={
                "response": [
                    {
                        "league": {"name": "Premier League", "id": 39},
                        "country": {"name": "England"},
                    }
                ]
            },
        )
    )
    client = ApiFootballClient()
    comp = client.fetch_competition(39, 2024)
    assert comp == {
        "name": "Premier League",
        "sport": "football",
        "country": "England",
        "season": "2024",
        "logo_url": None,
        "external_id": 39,
    }


@respx.mock
def test_api_football_fetch_competition_empty(monkeypatch):
    monkeypatch.setattr(config_module.settings, "api_football_key", "test-key")
    respx.get("https://v3.football.api-sports.io/leagues").mock(
        return_value=Response(200, json={"response": []})
    )
    client = ApiFootballClient()
    assert client.fetch_competition(999, 2024) is None


@respx.mock
def test_api_football_fetch_teams(monkeypatch):
    monkeypatch.setattr(config_module.settings, "api_football_key", "test-key")
    respx.get("https://v3.football.api-sports.io/teams").mock(
        return_value=Response(
            200,
            json={
                "response": [
                    {
                        "team": {
                            "name": "Arsenal",
                            "code": "ARS",
                            "country": "England",
                            "logo": "https://example.com/arsenal.png",
                        }
                    }
                ]
            },
        )
    )
    client = ApiFootballClient()
    teams = client.fetch_teams(39, 2024)
    assert len(teams) == 1
    assert teams[0] == {
        "name": "Arsenal",
        "short_name": "ARS",
        "country": "England",
        "logo_url": "https://example.com/arsenal.png",
        "external_id": None,
    }


@respx.mock
def test_api_football_fetch_matches(monkeypatch):
    monkeypatch.setattr(config_module.settings, "api_football_key", "test-key")
    respx.get("https://v3.football.api-sports.io/fixtures").mock(
        return_value=Response(
            200,
            json={
                "response": [
                    {
                        "fixture": {
                            "date": "2024-08-17T14:00:00+00:00",
                            "status": {"short": "FT"},
                        },
                        "teams": {
                            "home": {"name": "Arsenal"},
                            "away": {"name": "Wolves"},
                        },
                        "goals": {"home": 2, "away": 0},
                    }
                ]
            },
        )
    )
    client = ApiFootballClient()
    matches = client.fetch_matches(39, 2024)
    assert len(matches) == 1
    assert matches[0] == {
        "home_team": "Arsenal",
        "away_team": "Wolves",
        "kickoff_time": "2024-08-17T14:00:00+00:00",
        "status": "FT",
        "home_score": 2,
        "away_score": 0,
        "stage": None,
        "matchday": None,
        "group_name": None,
        "external_id": None,
    }


def test_api_football_missing_key_raises(monkeypatch):
    monkeypatch.setattr(config_module.settings, "api_football_key", "")
    client = ApiFootballClient()
    with pytest.raises(RuntimeError, match="API_FOOTBALL_KEY"):
        client.fetch_competition(39, 2024)
    with pytest.raises(RuntimeError, match="API_FOOTBALL_KEY"):
        client.fetch_teams(39, 2024)
    with pytest.raises(RuntimeError, match="API_FOOTBALL_KEY"):
        client.fetch_matches(39, 2024)


# ---------------------------------------------------------------------------
# Tank01
# ---------------------------------------------------------------------------

@respx.mock
def test_tank01_fetch_nfl_teams(monkeypatch):
    host = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    monkeypatch.setattr(config_module.settings, "tank01_key", "test-key")
    monkeypatch.setattr(config_module.settings, "tank01_host", host)
    respx.get(f"https://{host}/getNFLTeams").mock(
        return_value=Response(
            200,
            json={
                "body": [
                    {
                        "teamCity": "Kansas City",
                        "teamName": "Chiefs",
                        "conferenceAbv": "AFC",
                        "division": "AFC West",
                    }
                ]
            },
        )
    )
    client = Tank01Client()
    teams = client.fetch_nfl_teams()
    assert len(teams) == 1
    assert teams[0] == {
        "name": "Kansas City Chiefs",
        "conference": "AFC",
        "division": "AFC West",
        "abbreviation": None,
        "city": "Kansas City",
        "logo_url": None,
        "external_id": None,
    }


@respx.mock
def test_tank01_fetch_games(monkeypatch):
    host = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    monkeypatch.setattr(config_module.settings, "tank01_key", "test-key")
    monkeypatch.setattr(config_module.settings, "tank01_host", host)
    respx.get(f"https://{host}/getNFLGamesForWeek").mock(
        return_value=Response(
            200,
            json={
                "body": [
                    {
                        "home": "Kansas City Chiefs",
                        "away": "Baltimore Ravens",
                        "gameTime": "2025-09-07T13:00:00",
                        "gameStatus": "Scheduled",
                        "homePts": None,
                        "awayPts": None,
                    }
                ]
            },
        )
    )
    client = Tank01Client()
    games = client.fetch_games(game_week=1, season=2025)
    assert len(games) == 1
    assert games[0] == {
        "home_team": "Kansas City Chiefs",
        "away_team": "Baltimore Ravens",
        "kickoff_time": "2025-09-07T13:00:00",
        "status": "Scheduled",
        "home_score": None,
        "away_score": None,
        "external_id": None,
        "season": 2025,
        "season_type": "reg",
        "week": 1,
    }


def test_tank01_missing_key_raises(monkeypatch):
    monkeypatch.setattr(config_module.settings, "tank01_key", "")
    client = Tank01Client()
    with pytest.raises(RuntimeError, match="TANK01_KEY"):
        client.fetch_nfl_teams()
    with pytest.raises(RuntimeError, match="TANK01_KEY"):
        client.fetch_games()
