from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.logging_config import get_logger
from app.models import Competition, Injury, Match, Player, Standing, Team
from app.services.datasources import ApiFootballClient

logger = get_logger(__name__)
_BERLIN = ZoneInfo("Europe/Berlin")


def _parse_dt(value) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def import_bundesliga(db: Session, season: int = 2025, league_id: int = 78) -> dict:
    logger.info("import_bundesliga start (league_id=%s, season=%s)", league_id, season)
    created = {"competitions": 0, "teams": 0, "matches": 0}
    updated = {"competitions": 0, "teams": 0, "matches": 0}

    with ApiFootballClient() as client:
        comp_data = client.fetch_competition(league_id, season)
        if comp_data is None:
            logger.error(
                "fetch_competition returned None for league_id=%s season=%s",
                league_id,
                season,
            )
            return {"created": 0, "updated": 0}

        comp = (
            db.query(Competition)
            .filter_by(name=comp_data["name"], season=comp_data["season"])
            .first()
        )
        if comp is None:
            comp = Competition(**comp_data)
            db.add(comp)
            created["competitions"] += 1
        else:
            for k, v in comp_data.items():
                setattr(comp, k, v)
            updated["competitions"] += 1
        # Slug und external_id für Bundesliga setzen
        comp.slug = "bundesliga"
        comp.external_id = league_id
        db.flush()

        teams_data = client.fetch_teams(league_id, season)
        name_to_id: dict[str, int] = {}
        for td in teams_data:
            team = db.query(Team).filter_by(name=td["name"]).first()
            if team is None:
                team = Team(**td)
                db.add(team)
                db.flush()
                created["teams"] += 1
            else:
                for k, v in td.items():
                    setattr(team, k, v)
                updated["teams"] += 1
            name_to_id[team.name] = team.id

        matches_data = client.fetch_matches(league_id, season)
        now = datetime.now(_BERLIN)
        for md in matches_data:
            home_name = md.get("home_team")
            away_name = md.get("away_team")
            if home_name not in name_to_id or away_name not in name_to_id:
                logger.warning(
                    "Skipping match: unknown team(s) home=%s away=%s",
                    home_name,
                    away_name,
                )
                continue
            home_id = name_to_id[home_name]
            away_id = name_to_id[away_name]
            kickoff = _parse_dt(md.get("kickoff_time"))

            match = (
                db.query(Match)
                .filter_by(
                    competition_id=comp.id,
                    home_team_id=home_id,
                    away_team_id=away_id,
                    kickoff_time=kickoff,
                )
                .first()
            )
            if match is None:
                match = Match(
                    competition_id=comp.id,
                    home_team_id=home_id,
                    away_team_id=away_id,
                    kickoff_time=kickoff,
                    status=md.get("status"),
                    home_score=md.get("home_score"),
                    away_score=md.get("away_score"),
                    last_updated=now,
                )
                db.add(match)
                created["matches"] += 1
            else:
                match.status = md.get("status")
                match.home_score = md.get("home_score")
                match.away_score = md.get("away_score")
                match.last_updated = now
                updated["matches"] += 1

    db.commit()
    logger.info("import_bundesliga done: created=%s updated=%s", created, updated)
    return {
        "created": sum(created.values()),
        "updated": sum(updated.values()),
    }


def import_standings(db: Session, league_id: int, season: int, competition_id: int) -> dict:
    """Importiert die Tabelle eines Fußball-Wettbewerbs."""
    logger.info("import_standings start (league_id=%s, season=%s, comp=%s)", league_id, season, competition_id)

    with ApiFootballClient() as client:
        standings_data = client.fetch_standings(league_id, season)

    # Bestehende Standings für diesen Wettbewerb löschen
    db.query(Standing).filter_by(competition_id=competition_id).delete()
    db.flush()

    imported = 0
    for sd in standings_data:
        team = db.query(Team).filter_by(name=sd["team_name"]).first()
        if team is None:
            logger.warning("import_standings: team not found: %s", sd["team_name"])
            continue
        standing = Standing(
            competition_id=competition_id,
            team_id=team.id,
            group_name=sd.get("group"),
            rank=sd.get("rank"),
            played=sd.get("played", 0),
            won=sd.get("won", 0),
            draw=sd.get("draw", 0),
            lost=sd.get("lost", 0),
            goals_for=sd.get("goals_for", 0),
            goals_against=sd.get("goals_against", 0),
            goal_difference=sd.get("goal_difference", 0),
            points=sd.get("points", 0),
        )
        db.add(standing)
        imported += 1

    db.commit()
    logger.info("import_standings done: imported=%s", imported)
    return {"imported": imported}


def import_injuries(db: Session, league_id: int, season: int) -> dict:
    """Importiert Verletzungen für einen Fußball-Wettbewerb."""
    logger.info("import_injuries start (league_id=%s, season=%s)", league_id, season)

    with ApiFootballClient() as client:
        injuries_data = client.fetch_injuries(league_id, season)

    from datetime import date as date_type

    created = updated = 0
    for inj in injuries_data:
        team = db.query(Team).filter_by(name=inj.get("team_name")).first()
        if team is None:
            logger.warning("import_injuries: team not found: %s", inj.get("team_name"))
            continue

        ext_id = inj.get("player_external_id")
        if ext_id is not None:
            player = db.query(Player).filter_by(external_id=ext_id).first()
        else:
            player = (
                db.query(Player)
                .filter_by(name=inj["player_name"], team_id=team.id)
                .first()
            )

        if player is None:
            player = Player(
                name=inj["player_name"],
                team_id=team.id,
                position=inj.get("position"),
                age=inj.get("age"),
                external_id=ext_id,
            )
            db.add(player)
            db.flush()
            created += 1
        else:
            player.position = inj.get("position")
            player.age = inj.get("age")
            updated += 1

        # Bestehende Verletzungen des Spielers löschen und neu einfügen
        db.query(Injury).filter_by(player_id=player.id).delete()
        injury = Injury(
            player_id=player.id,
            team_id=team.id,
            description=inj.get("description"),
            status=inj.get("status"),
        )
        db.add(injury)

    db.commit()
    logger.info("import_injuries done: players created=%s updated=%s", created, updated)
    return {"created": created, "updated": updated}


def import_football_competition(db: Session, league_id: int, season: int) -> dict:
    """Importiert einen Fußball-Wettbewerb komplett: Teams, Spiele, Tabelle und Verletzte."""
    result_main = import_bundesliga(db, season=season, league_id=league_id)

    # competition_id nachschlagen
    comp = (
        db.query(Competition)
        .filter(Competition.external_id == league_id, Competition.season == str(season))
        .first()
    )
    if comp is None:
        logger.warning("import_football_competition: competition not found after import")
        return result_main

    result_standings = import_standings(db, league_id, season, comp.id)
    result_injuries = import_injuries(db, league_id, season)

    return {
        "main": result_main,
        "standings": result_standings,
        "injuries": result_injuries,
    }
