from datetime import datetime, timezone

from app.config import settings
from app.services.datasources.base import BaseDataSource


def _session_status(date_end_str: str | None) -> str:
    """Leitet den Session-Status aus dem geplanten Endzeitpunkt ab.

    OpenF1 liefert ``date_end`` immer — auch für zukünftige Sessions.
    Wir müssen deshalb explizit prüfen ob der Zeitpunkt in der Vergangenheit liegt.
    """
    if not date_end_str:
        return "upcoming"
    try:
        date_end = datetime.fromisoformat(date_end_str)
        # sicherstellen dass timezone-aware verglichen wird
        if date_end.tzinfo is None:
            date_end = date_end.replace(tzinfo=timezone.utc)
        return "completed" if date_end < datetime.now(timezone.utc) else "upcoming"
    except (ValueError, TypeError):
        return "upcoming"


class OpenF1Client(BaseDataSource):
    def __init__(self):
        super().__init__(base_url=settings.openf1_base_url)

    def fetch_races(self, year: int) -> list[dict]:
        resp = self._get("/meetings", params={"year": year})
        meetings = resp.json()
        result = []
        for m in meetings:
            name = m.get("meeting_official_name") or m.get("meeting_name", "")
            result.append({
                "season": str(year),
                "name": name,
                "date": m.get("date_start"),
                "status": "scheduled",
                "location": m.get("location"),
                "country": m.get("country_name"),
                "round": None,  # OpenF1 liefert keine Lauf-Nummer
                "external_id": m.get("meeting_key"),
            })
        return result

    def fetch_drivers(self, session_key: str = "latest") -> list[dict]:
        resp = self._get("/drivers", params={"session_key": session_key})
        drivers = resp.json()
        seen = set()
        result = []
        for d in drivers:
            number = d.get("driver_number")
            if number in seen:
                continue
            seen.add(number)
            full_name = d.get("full_name") or f"{d.get('first_name', '')} {d.get('last_name', '')}".strip()
            result.append({
                "name": full_name,
                "team": d.get("team_name"),
                "number": number,
                "abbreviation": d.get("name_acronym"),
                "country": d.get("country_code"),
                "team_color": d.get("team_colour"),
                "external_id": number,
            })
        return result

    def fetch_sessions(self, meeting_key: int) -> list[dict]:
        resp = self._get("/sessions", params={"meeting_key": meeting_key})
        sessions = resp.json()
        result = []
        for s in sessions:
            result.append({
                "external_id": s.get("session_key"),
                "name": s.get("session_name"),
                "session_type": s.get("session_type"),
                "start_time": s.get("date_start"),
                "end_time": s.get("date_end"),  # geplantes/tatsächliches Ende
                "status": _session_status(s.get("date_end")),
            })
        return result

    def fetch_session_results(self, session_key: int) -> list[dict]:
        # OpenF1-Endpoint heißt /session_result (nicht /results)
        resp = self._get("/session_result", params={"session_key": session_key})
        results = resp.json()
        out = []
        for r in results:
            duration = r.get("duration")
            if r.get("dsq"):
                status = "DSQ"
            elif r.get("dns"):
                status = "DNS"
            elif r.get("dnf"):
                status = "DNF"
            else:
                status = "Finished"
            out.append({
                "driver_number": r.get("driver_number"),
                "position": r.get("position"),
                "time": str(duration) if duration is not None else None,
                "laps": r.get("number_of_laps"),  # korrekter Feldname laut OpenF1-Docs
                "points": None,  # /session_result liefert keine Punktefelder
                "status": status,
            })
        return out

    def fetch_championship_drivers(self, session_key: int) -> list[dict]:
        """WM-Stand der Fahrer nach einer Race-Session.

        OpenF1-Endpoint: /championship_drivers (Beta, nur für Race-Sessions).
        Liefert aktuelle und vorherige Punkte sowie Position.
        """
        resp = self._get("/championship_drivers", params={"session_key": session_key})
        return [
            {
                "driver_number": d.get("driver_number"),
                "points": d.get("points_current", 0) or 0,
                "position": d.get("position_current"),
            }
            for d in resp.json()
        ]

    def fetch_championship_teams(self, session_key: int) -> list[dict]:
        """WM-Stand der Konstrukteure nach einer Race-Session.

        OpenF1-Endpoint: /championship_teams (Beta, nur für Race-Sessions).
        """
        resp = self._get("/championship_teams", params={"session_key": session_key})
        return [
            {
                "team_name": d.get("team_name"),
                "points": d.get("points_current", 0) or 0,
                "position": d.get("position_current"),
            }
            for d in resp.json()
        ]
