import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base, Competition, Driver, Match, NflTeam, Race, Team
from app.services.datasources import ApiFootballClient, OpenF1Client, Tank01Client
from app.services.f1_service import import_f1_drivers, import_f1_races
from app.services.football_service import import_bundesliga
from app.services.nfl_service import import_nfl_games, import_nfl_teams


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# ─── F1 Races ────────────────────────────────────────────────────────────────

_F1_RACES = [{"season": "2025", "name": "Test GP", "date": None, "status": "scheduled"}]


def test_import_f1_races_creates(db, monkeypatch):
    monkeypatch.setattr(OpenF1Client, "fetch_races", lambda self, year=2025: list(_F1_RACES))
    result = import_f1_races(db)
    assert result["created"] == 1
    assert result["updated"] == 0
    assert db.query(Race).count() == 1


def test_import_f1_races_no_duplicate(db, monkeypatch):
    monkeypatch.setattr(OpenF1Client, "fetch_races", lambda self, year=2025: list(_F1_RACES))
    import_f1_races(db)
    result = import_f1_races(db)
    assert result["created"] == 0
    assert result["updated"] == 1
    assert db.query(Race).count() == 1


# ─── F1 Drivers ──────────────────────────────────────────────────────────────

_F1_DRIVERS = [{"name": "Max Verstappen", "team": "Red Bull Racing", "number": 1}]


def test_import_f1_drivers_creates(db, monkeypatch):
    monkeypatch.setattr(
        OpenF1Client,
        "fetch_drivers",
        lambda self, session_key="latest": list(_F1_DRIVERS),
    )
    result = import_f1_drivers(db)
    assert result["created"] == 1
    assert db.query(Driver).count() == 1


def test_import_f1_drivers_no_duplicate(db, monkeypatch):
    monkeypatch.setattr(
        OpenF1Client,
        "fetch_drivers",
        lambda self, session_key="latest": list(_F1_DRIVERS),
    )
    import_f1_drivers(db)
    result = import_f1_drivers(db)
    assert result["created"] == 0
    assert result["updated"] == 1
    assert db.query(Driver).count() == 1


# ─── Football (Bundesliga) ────────────────────────────────────────────────────

_COMP_DATA = {
    "name": "Bundesliga",
    "sport": "football",
    "country": "Germany",
    "season": "2025",
}
_TEAMS_DATA = [
    {"name": "Bayern Munich", "short_name": "BAY", "country": "Germany", "logo_url": None},
    {"name": "Borussia Dortmund", "short_name": "BVB", "country": "Germany", "logo_url": None},
]
_MATCHES_DATA = [
    {
        "home_team": "Bayern Munich",
        "away_team": "Borussia Dortmund",
        "kickoff_time": "2025-08-01T15:30:00",
        "status": "NS",
        "home_score": None,
        "away_score": None,
    }
]


def _patch_football(monkeypatch):
    monkeypatch.setattr(
        ApiFootballClient,
        "fetch_competition",
        lambda self, league_id, season: dict(_COMP_DATA),
    )
    monkeypatch.setattr(
        ApiFootballClient,
        "fetch_teams",
        lambda self, league_id, season: [dict(t) for t in _TEAMS_DATA],
    )
    monkeypatch.setattr(
        ApiFootballClient,
        "fetch_matches",
        lambda self, league_id, season: [dict(m) for m in _MATCHES_DATA],
    )


def test_import_bundesliga_creates(db, monkeypatch):
    _patch_football(monkeypatch)
    result = import_bundesliga(db)
    # 1 competition + 2 teams + 1 match = 4
    assert result["created"] == 4
    assert result["updated"] == 0


def test_import_bundesliga_no_duplicate(db, monkeypatch):
    _patch_football(monkeypatch)
    import_bundesliga(db)
    result = import_bundesliga(db)
    assert result["created"] == 0
    assert db.query(Competition).count() == 1
    assert db.query(Team).count() == 2
    assert db.query(Match).count() == 1


def test_import_bundesliga_match_fk(db, monkeypatch):
    _patch_football(monkeypatch)
    import_bundesliga(db)
    match = db.query(Match).first()
    assert match is not None
    home = db.query(Team).filter_by(name="Bayern Munich").first()
    away = db.query(Team).filter_by(name="Borussia Dortmund").first()
    assert match.home_team_id == home.id
    assert match.away_team_id == away.id


# ─── NFL Teams ────────────────────────────────────────────────────────────────

_NFL_TEAMS = [
    {"name": "Kansas City Chiefs", "conference": "AFC", "division": "West"},
    {"name": "San Francisco 49ers", "conference": "NFC", "division": "West"},
]


def test_import_nfl_teams_creates(db, monkeypatch):
    monkeypatch.setattr(Tank01Client, "fetch_nfl_teams", lambda self: [dict(t) for t in _NFL_TEAMS])
    result = import_nfl_teams(db)
    assert result["created"] == 2
    assert db.query(NflTeam).count() == 2


def test_import_nfl_teams_no_duplicate(db, monkeypatch):
    monkeypatch.setattr(Tank01Client, "fetch_nfl_teams", lambda self: [dict(t) for t in _NFL_TEAMS])
    import_nfl_teams(db)
    result = import_nfl_teams(db)
    assert result["created"] == 0
    assert result["updated"] == 2
    assert db.query(NflTeam).count() == 2


# ─── NFL Games ────────────────────────────────────────────────────────────────

_NFL_GAMES = [
    {
        "home_team": "Kansas City Chiefs",
        "away_team": "San Francisco 49ers",
        "kickoff_time": "2025-09-05T20:20:00",
        "status": "Scheduled",
        "home_score": None,
        "away_score": None,
    }
]


def test_import_nfl_games_creates(db, monkeypatch):
    monkeypatch.setattr(
        Tank01Client,
        "fetch_games",
        lambda self, game_week=1, season=2025, season_type="reg": [dict(g) for g in _NFL_GAMES],
    )
    result = import_nfl_games(db)
    # 2 teams + 1 match = 3
    assert result["created"] == 3
    assert db.query(Match).count() == 1
    assert db.query(Competition).filter_by(name="NFL").count() == 1


def test_import_nfl_games_no_duplicate(db, monkeypatch):
    monkeypatch.setattr(
        Tank01Client,
        "fetch_games",
        lambda self, game_week=1, season=2025, season_type="reg": [dict(g) for g in _NFL_GAMES],
    )
    import_nfl_games(db)
    result = import_nfl_games(db)
    assert result["created"] == 0
    assert db.query(Match).count() == 1
