from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.services.f1_service import (
    import_f1_drivers,
    import_f1_races,
    import_f1_session_results,
    import_f1_sessions,
    import_f1_standings,
)
from app.services.football_service import import_bundesliga, import_football_competition
from app.services.nfl_service import (
    import_nfl_games,
    import_nfl_games_new,
    import_nfl_standings,
    import_nfl_teams,
)

router = APIRouter(prefix="/admin", dependencies=[Depends(require_admin)])


@router.post("/import/bundesliga")
def admin_import_bundesliga(
    season: int = 2025,
    league_id: int = 78,
    db: Session = Depends(get_db),
):
    return import_bundesliga(db, season=season, league_id=league_id)


@router.post("/import/football")
def admin_import_football(
    league_id: int = 78,
    season: int = 2025,
    db: Session = Depends(get_db),
):
    """Importiert einen Fußball-Wettbewerb komplett: Teams, Spiele, Tabelle, Verletzte."""
    return import_football_competition(db, league_id=league_id, season=season)


@router.post("/import/f1/races")
def admin_import_f1_races(year: int = 2025, db: Session = Depends(get_db)):
    return import_f1_races(db, year=year)


@router.post("/import/f1/drivers")
def admin_import_f1_drivers(session_key: str = "latest", db: Session = Depends(get_db)):
    return import_f1_drivers(db, session_key=session_key)


@router.post("/import/f1/sessions")
def admin_import_f1_sessions(year: int = 2025, db: Session = Depends(get_db)):
    """Importiert F1-Sessions für alle Rennen eines Jahres."""
    return import_f1_sessions(db, year=year)


@router.post("/import/f1/session-results")
def admin_import_f1_session_results(session_key: int, db: Session = Depends(get_db)):
    """Importiert Ergebnisse einer einzelnen F1-Session (via OpenF1 session_key)."""
    return import_f1_session_results(db, session_key=session_key)


@router.post("/import/f1/standings")
def admin_import_f1_standings(year: int = 2025, db: Session = Depends(get_db)):
    """Berechnet F1-Standings aus den vorhandenen Session-Ergebnissen."""
    return import_f1_standings(db, year=year)


@router.post("/import/nfl/teams")
def admin_import_nfl_teams(db: Session = Depends(get_db)):
    return import_nfl_teams(db)


@router.post("/import/nfl/games")
def admin_import_nfl_games(
    game_week: int = 1,
    season: int = 2025,
    season_type: str = "reg",
    db: Session = Depends(get_db),
):
    return import_nfl_games(db, game_week=game_week, season=season, season_type=season_type)


@router.post("/import/nfl/games-new")
def admin_import_nfl_games_new(
    week: int = 1,
    season: int = 2025,
    season_type: str = "reg",
    db: Session = Depends(get_db),
):
    """Importiert NFL-Spiele in die neue nfl_games-Tabelle (per NflTeam-Abkürzung)."""
    return import_nfl_games_new(db, game_week=week, season=season, season_type=season_type)


@router.post("/import/nfl/standings")
def admin_import_nfl_standings(season: int = 2025, db: Session = Depends(get_db)):
    """Importiert NFL-Standings (W/L/D) für eine Saison."""
    return import_nfl_standings(db, season=season)
