import types
from datetime import datetime

from app.schemas import (
    CompetitionRead,
    DriverRead,
    MatchRead,
    NflTeamRead,
    RaceRead,
    TeamRead,
)


def make_obj(**kwargs):
    return types.SimpleNamespace(**kwargs)


def test_competition_read():
    obj = make_obj(id=1, name="Bundesliga", sport="football", country="Germany", season="2025/26")
    schema = CompetitionRead.model_validate(obj)
    assert schema.id == 1
    assert schema.name == "Bundesliga"
    assert schema.sport == "football"
    assert schema.country == "Germany"
    assert schema.season == "2025/26"


def test_competition_read_optional_none():
    obj = make_obj(id=2, name="La Liga", sport="football", country=None, season=None)
    schema = CompetitionRead.model_validate(obj)
    assert schema.country is None
    assert schema.season is None


def test_team_read():
    obj = make_obj(id=1, name="Bayern Munich", short_name="FCB", country="Germany", logo_url="http://example.com/logo.png")
    schema = TeamRead.model_validate(obj)
    assert schema.id == 1
    assert schema.name == "Bayern Munich"
    assert schema.short_name == "FCB"
    assert schema.country == "Germany"
    assert schema.logo_url == "http://example.com/logo.png"


def test_team_read_optional_none():
    obj = make_obj(id=2, name="Some Team", short_name=None, country=None, logo_url=None)
    schema = TeamRead.model_validate(obj)
    assert schema.short_name is None
    assert schema.logo_url is None


def test_match_read():
    now = datetime(2025, 8, 1, 18, 0, 0)
    updated = datetime(2025, 8, 1, 20, 0, 0)
    obj = make_obj(
        id=10,
        competition_id=1,
        home_team_id=2,
        away_team_id=3,
        kickoff_time=now,
        status="finished",
        home_score=2,
        away_score=1,
        last_updated=updated,
    )
    schema = MatchRead.model_validate(obj)
    assert schema.id == 10
    assert schema.competition_id == 1
    assert schema.home_team_id == 2
    assert schema.away_team_id == 3
    assert schema.kickoff_time == now
    assert schema.status == "finished"
    assert schema.home_score == 2
    assert schema.away_score == 1
    assert schema.last_updated == updated


def test_match_read_optional_none():
    obj = make_obj(
        id=11,
        competition_id=1,
        home_team_id=2,
        away_team_id=3,
        kickoff_time=None,
        status=None,
        home_score=None,
        away_score=None,
        last_updated=None,
    )
    schema = MatchRead.model_validate(obj)
    assert schema.kickoff_time is None
    assert schema.last_updated is None


def test_driver_read():
    obj = make_obj(id=1, name="Max Verstappen", team="Red Bull", number=1)
    schema = DriverRead.model_validate(obj)
    assert schema.id == 1
    assert schema.name == "Max Verstappen"
    assert schema.team == "Red Bull"
    assert schema.number == 1


def test_driver_read_optional_none():
    obj = make_obj(id=2, name="Some Driver", team=None, number=None)
    schema = DriverRead.model_validate(obj)
    assert schema.team is None
    assert schema.number is None


def test_race_read():
    race_date = datetime(2025, 3, 16, 15, 0, 0)
    obj = make_obj(id=1, season="2025", name="Bahrain GP", date=race_date, status="finished")
    schema = RaceRead.model_validate(obj)
    assert schema.id == 1
    assert schema.season == "2025"
    assert schema.name == "Bahrain GP"
    assert schema.date == race_date
    assert schema.status == "finished"


def test_race_read_optional_none():
    obj = make_obj(id=2, season=None, name="Unknown Race", date=None, status=None)
    schema = RaceRead.model_validate(obj)
    assert schema.season is None
    assert schema.date is None
    assert schema.status is None


def test_nfl_team_read():
    obj = make_obj(id=1, name="Kansas City Chiefs", conference="AFC", division="West")
    schema = NflTeamRead.model_validate(obj)
    assert schema.id == 1
    assert schema.name == "Kansas City Chiefs"
    assert schema.conference == "AFC"
    assert schema.division == "West"


def test_nfl_team_read_optional_none():
    obj = make_obj(id=2, name="Some Team", conference=None, division=None)
    schema = NflTeamRead.model_validate(obj)
    assert schema.conference is None
    assert schema.division is None
