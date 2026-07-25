from datetime import datetime as _dt
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, union
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.logging_config import get_logger
from app.models import Competition, Injury, Match, Player, Standing, Team
from app.schemas import InjuryWithPlayer, MatchRead, StandingRead, TeamRead
from app.services.football_service import import_bundesliga, import_injuries, import_standings

router = APIRouter(prefix="/bundesliga")
logger = get_logger(__name__)

_BUNDESLIGA_LEAGUE_ID = 78  # API-Football ID für die Bundesliga


def _get_bundesliga_competition(db: Session, season: Optional[str]) -> Optional[Competition]:
    q = db.query(Competition).filter(
        Competition.sport == "football",
        Competition.name == "Bundesliga",
    )
    if season is not None:
        q = q.filter(Competition.season == season)
    return q.first()


def _auto_import_bundesliga(db: Session, season: Optional[str]) -> None:
    """Lädt Bundesliga-Daten von API-Football wenn die DB leer ist."""
    try:
        season_int = int(season) if season else _dt.now().year
        import_bundesliga(db, season=season_int, league_id=_BUNDESLIGA_LEAGUE_ID)
    except Exception:
        logger.warning("Auto-import Bundesliga fehlgeschlagen", exc_info=True)


@router.get("/table", response_model=list[TeamRead])
def get_bundesliga_table(season: Optional[str] = None, db: Session = Depends(get_db)):
    comp = _get_bundesliga_competition(db, season)
    if comp is None:
        _auto_import_bundesliga(db, season)
        comp = _get_bundesliga_competition(db, season)
    if comp is None:
        return []
    team_ids_stmt = union(
        select(Match.home_team_id).where(Match.competition_id == comp.id),
        select(Match.away_team_id).where(Match.competition_id == comp.id),
    ).subquery()
    return db.query(Team).filter(Team.id.in_(select(team_ids_stmt))).all()


@router.get("/matches", response_model=list[MatchRead])
def get_bundesliga_matches(season: Optional[str] = None, db: Session = Depends(get_db)):
    comp = _get_bundesliga_competition(db, season)
    if comp is None:
        _auto_import_bundesliga(db, season)
        comp = _get_bundesliga_competition(db, season)
    if comp is None:
        return []
    matches = db.query(Match).filter(Match.competition_id == comp.id).all()
    if not matches:
        _auto_import_bundesliga(db, season)
        matches = db.query(Match).filter(Match.competition_id == comp.id).all()
    return matches


@router.get("/standings", response_model=list[StandingRead])
def get_bundesliga_standings(
    season: Optional[str] = None,
    group: Optional[str] = None,
    db: Session = Depends(get_db),
):
    comp = _get_bundesliga_competition(db, season)
    if comp is None:
        _auto_import_bundesliga(db, season)
        comp = _get_bundesliga_competition(db, season)
    if comp is None:
        return []
    q = db.query(Standing).filter(Standing.competition_id == comp.id)
    if group is not None:
        q = q.filter(Standing.group_name == group)
    standings = q.order_by(Standing.rank).all()
    if not standings:
        try:
            league_id = comp.external_id or _BUNDESLIGA_LEAGUE_ID
            season_int = int(season) if season else _dt.now().year
            import_standings(db, league_id=league_id, season=season_int, competition_id=comp.id)
        except Exception:
            logger.warning("Auto-import Bundesliga-Tabelle fehlgeschlagen", exc_info=True)
        q2 = db.query(Standing).filter(Standing.competition_id == comp.id)
        if group is not None:
            q2 = q2.filter(Standing.group_name == group)
        standings = q2.order_by(Standing.rank).all()
    return standings


@router.get("/injuries", response_model=list[InjuryWithPlayer])
def get_bundesliga_injuries(
    season: Optional[str] = None,
    team_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Injury, Player).join(Player, Injury.player_id == Player.id)
    if team_id is not None:
        q = q.filter(Injury.team_id == team_id)
    rows = q.all()
    if not rows:
        try:
            comp = _get_bundesliga_competition(db, season)
            league_id = (comp.external_id if comp else None) or _BUNDESLIGA_LEAGUE_ID
            season_int = int(season) if season else _dt.now().year
            import_injuries(db, league_id=league_id, season=season_int)
        except Exception:
            logger.warning("Auto-import Bundesliga-Verletzte fehlgeschlagen", exc_info=True)
        q2 = db.query(Injury, Player).join(Player, Injury.player_id == Player.id)
        if team_id is not None:
            q2 = q2.filter(Injury.team_id == team_id)
        rows = q2.all()
    return [
        InjuryWithPlayer(
            id=injury.id,
            player_name=player.name,
            position=player.position,
            age=player.age,
            description=injury.description,
            since=injury.since,
            missed_matches=injury.missed_matches,
            status=injury.status,
        )
        for injury, player in rows
    ]
