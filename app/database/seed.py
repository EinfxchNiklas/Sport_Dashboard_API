from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.logging_config import get_logger
from app.models import Base, Competition, Driver, Match, NflTeam, Race, Team

_BERLIN = ZoneInfo("Europe/Berlin")
logger = get_logger(__name__)


def seed(db: Session) -> None:
    # Competition
    competition = db.query(Competition).filter_by(
        name="Bundesliga", sport="football", season="2025"
    ).first()
    if competition is None:
        competition = Competition(
            name="Bundesliga",
            sport="football",
            country="Germany",
            season="2025",
        )
        db.add(competition)
        db.flush()
        logger.info("Inserted Competition: Bundesliga")
    else:
        logger.info("Skipped Competition: Bundesliga (already exists)")

    # Teams
    fcb = db.query(Team).filter_by(name="FC Bayern München").first()
    if fcb is None:
        fcb = Team(name="FC Bayern München", short_name="FCB", country="Germany")
        db.add(fcb)
        db.flush()
        logger.info("Inserted Team: FC Bayern München")
    else:
        logger.info("Skipped Team: FC Bayern München (already exists)")

    bvb = db.query(Team).filter_by(name="Borussia Dortmund").first()
    if bvb is None:
        bvb = Team(name="Borussia Dortmund", short_name="BVB", country="Germany")
        db.add(bvb)
        db.flush()
        logger.info("Inserted Team: Borussia Dortmund")
    else:
        logger.info("Skipped Team: Borussia Dortmund (already exists)")

    # Match
    match = (
        db.query(Match)
        .filter_by(
            competition_id=competition.id,
            home_team_id=fcb.id,
            away_team_id=bvb.id,
        )
        .first()
    )
    if match is None:
        match = Match(
            competition_id=competition.id,
            home_team_id=fcb.id,
            away_team_id=bvb.id,
            kickoff_time=datetime(2025, 9, 20, 15, 30, tzinfo=_BERLIN),
            status="scheduled",
            home_score=None,
            away_score=None,
            last_updated=datetime.now(_BERLIN),
        )
        db.add(match)
        logger.info("Inserted Match: FC Bayern München vs Borussia Dortmund")
    else:
        logger.info("Skipped Match: FC Bayern München vs Borussia Dortmund (already exists)")

    # Race
    race = db.query(Race).filter_by(name="Test Grand Prix", season="2025").first()
    if race is None:
        race = Race(
            name="Test Grand Prix",
            season="2025",
            date=datetime(2025, 10, 5, 14, 0, tzinfo=_BERLIN),
            status="scheduled",
        )
        db.add(race)
        logger.info("Inserted Race: Test Grand Prix")
    else:
        logger.info("Skipped Race: Test Grand Prix (already exists)")

    # Driver
    driver = db.query(Driver).filter_by(name="Max Mustermann").first()
    if driver is None:
        driver = Driver(name="Max Mustermann", team="Test Racing", number=1)
        db.add(driver)
        logger.info("Inserted Driver: Max Mustermann")
    else:
        logger.info("Skipped Driver: Max Mustermann (already exists)")

    # NflTeam
    nfl_team = db.query(NflTeam).filter_by(name="Kansas City Chiefs").first()
    if nfl_team is None:
        nfl_team = NflTeam(name="Kansas City Chiefs", conference="AFC", division="West")
        db.add(nfl_team)
        logger.info("Inserted NflTeam: Kansas City Chiefs")
    else:
        logger.info("Skipped NflTeam: Kansas City Chiefs (already exists)")

    db.commit()


if __name__ == "__main__":
    from app.database.session import SessionLocal, engine

    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        seed(db)
        print("Seed erfolgreich abgeschlossen.")
    finally:
        db.close()
