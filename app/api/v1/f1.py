from datetime import datetime as _dt
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.logging_config import get_logger
from app.models import ConstructorStanding, Driver, DriverStanding, Race, RaceSession, SessionResult
from app.schemas import (
    ConstructorStandingRead,
    DriverRead,
    DriverStandingRead,
    RaceRead,
    RaceSessionRead,
    SessionResultRead,
)
from app.services.f1_service import (
    import_f1_drivers,
    import_f1_races,
    import_f1_session_results,
    import_f1_sessions,
    import_f1_sessions_for_race,
    import_f1_standings,
)

router = APIRouter(prefix="/f1")
logger = get_logger(__name__)


def _current_year() -> int:
    return _dt.now().year


@router.get("/races", response_model=list[RaceRead])
def get_f1_races(season: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Race)
    if season:
        q = q.filter(Race.season == season)
    races = q.all()
    if not races:
        try:
            year = int(season) if season else _current_year()
            import_f1_races(db, year=year)
            import_f1_drivers(db)
        except Exception:
            logger.warning("Auto-import F1 Rennen fehlgeschlagen", exc_info=True)
        q2 = db.query(Race)
        if season:
            q2 = q2.filter(Race.season == season)
        races = q2.all()
    return races


@router.get("/drivers", response_model=list[DriverRead])
def get_f1_drivers(db: Session = Depends(get_db)):
    drivers = db.query(Driver).all()
    if not drivers:
        try:
            import_f1_drivers(db)
        except Exception:
            logger.warning("Auto-import F1 Fahrer fehlgeschlagen", exc_info=True)
        drivers = db.query(Driver).all()
    return drivers


@router.get("/races/{race_id}/sessions", response_model=list[RaceSessionRead])
def get_race_sessions(race_id: int, db: Session = Depends(get_db)):
    race = db.get(Race, race_id)
    if race is None:
        raise HTTPException(status_code=404, detail="Rennen nicht gefunden")
    sessions = (
        db.query(RaceSession)
        .filter(RaceSession.race_id == race_id)
        .order_by(RaceSession.start_time)
        .all()
    )
    if not sessions:
        try:
            year = int(race.season) if race.season else _current_year()
            if not race.external_id:
                import_f1_races(db, year=year)
                db.refresh(race)
            if race.external_id:
                # Gezielter Import nur für dieses Rennen (ein HTTP-Request statt ~20)
                import_f1_sessions_for_race(db, race)
        except Exception:
            logger.warning("Auto-import F1 Sessions für race_id=%s fehlgeschlagen", race_id, exc_info=True)
        sessions = (
            db.query(RaceSession)
            .filter(RaceSession.race_id == race_id)
            .order_by(RaceSession.start_time)
            .all()
        )
    return sessions


@router.get("/sessions/{session_id}/results", response_model=list[SessionResultRead])
def get_session_results(session_id: int, db: Session = Depends(get_db)):
    race_session = db.get(RaceSession, session_id)
    if race_session is None:
        raise HTTPException(status_code=404, detail="Session nicht gefunden")
    results = (
        db.query(SessionResult)
        .filter(SessionResult.session_id == session_id)
        .order_by(SessionResult.position)
        .all()
    )
    if not results:
        try:
            # Falls external_id fehlt → Session-Import nachholen
            if not race_session.external_id:
                race = db.get(Race, race_session.race_id)
                if race:
                    year = int(race.season) if race.season else _current_year()
                    if not race.external_id:
                        import_f1_races(db, year=year)
                        db.refresh(race)
                    if race.external_id:
                        import_f1_sessions(db, year=year)
                        db.refresh(race_session)
            if race_session.external_id:
                if not db.query(Driver).first():
                    import_f1_drivers(db)
                import_f1_session_results(db, session_key=race_session.external_id)
        except Exception:
            logger.warning(
                "Auto-import F1 Session-Ergebnisse für session_id=%s fehlgeschlagen",
                session_id,
                exc_info=True,
            )
        results = (
            db.query(SessionResult)
            .filter(SessionResult.session_id == session_id)
            .order_by(SessionResult.position)
            .all()
        )
    return results


@router.get("/standings/drivers", response_model=list[DriverStandingRead])
def get_driver_standings(season: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(DriverStanding)
    if season:
        q = q.filter(DriverStanding.season == season)
    standings = q.order_by(DriverStanding.position).all()
    if not standings:
        try:
            year = int(season) if season else _current_year()
            import_f1_standings(db, year=year)
        except Exception:
            logger.warning("Auto-import F1 Fahrer-Standings fehlgeschlagen", exc_info=True)
        q2 = db.query(DriverStanding)
        if season:
            q2 = q2.filter(DriverStanding.season == season)
        standings = q2.order_by(DriverStanding.position).all()
    return standings


@router.get("/standings/constructors", response_model=list[ConstructorStandingRead])
def get_constructor_standings(season: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(ConstructorStanding)
    if season:
        q = q.filter(ConstructorStanding.season == season)
    standings = q.order_by(ConstructorStanding.position).all()
    if not standings:
        try:
            year = int(season) if season else _current_year()
            import_f1_standings(db, year=year)
        except Exception:
            logger.warning("Auto-import F1 Konstrukteurs-Standings fehlgeschlagen", exc_info=True)
        q2 = db.query(ConstructorStanding)
        if season:
            q2 = q2.filter(ConstructorStanding.season == season)
        standings = q2.order_by(ConstructorStanding.position).all()
    return standings
