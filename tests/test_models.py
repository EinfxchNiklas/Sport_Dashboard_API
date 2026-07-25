from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base, Competition, Team, Match

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)


def test_create_competition():
    with Session(engine) as session:
        comp = Competition(name="Bundesliga", sport="football", country="Germany", season="2025/26")
        session.add(comp)
        session.commit()
        fetched = session.get(Competition, comp.id)
        assert fetched is not None
        assert fetched.name == "Bundesliga"
        assert fetched.sport == "football"
        assert fetched.country == "Germany"
        assert fetched.season == "2025/26"


def test_create_teams_and_match():
    with Session(engine) as session:
        comp = Competition(name="Premier League", sport="football")
        home = Team(name="Arsenal FC", short_name="ARS", country="England")
        away = Team(name="Chelsea FC", short_name="CHE", country="England")
        session.add_all([comp, home, away])
        session.flush()

        match = Match(
            competition_id=comp.id,
            home_team_id=home.id,
            away_team_id=away.id,
            status="scheduled",
            home_score=None,
            away_score=None,
        )
        session.add(match)
        session.commit()

        fetched = session.get(Match, match.id)
        assert fetched is not None
        assert fetched.competition_id == comp.id
        assert fetched.home_team_id == home.id
        assert fetched.away_team_id == away.id
        assert fetched.status == "scheduled"


def test_match_last_updated_auto_set():
    with Session(engine) as session:
        comp = Competition(name="La Liga", sport="football")
        home = Team(name="Real Madrid")
        away = Team(name="FC Barcelona")
        session.add_all([comp, home, away])
        session.flush()

        match = Match(
            competition_id=comp.id,
            home_team_id=home.id,
            away_team_id=away.id,
        )
        session.add(match)
        session.commit()

        fetched = session.get(Match, match.id)
        assert fetched.last_updated is not None
