from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    kickoff_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]]
    home_score: Mapped[Optional[int]]
    away_score: Mapped[Optional[int]]
    # Phase des Wettbewerbs, technischer Schlüssel:
    # "group" | "league_phase" | "play_offs" | "round_of_32" | "round_of_16"
    # | "quarter_final" | "semi_final" | "final" ...
    stage: Mapped[Optional[str]] = mapped_column(index=True)
    # Anzeigename der Runde (z. B. "Sechzehntelfinale", "Ligaphase", "Finale")
    round_name: Mapped[Optional[str]]
    # Spieltag innerhalb einer Liga-/Gruppenphase (Bundesliga, CL-Ligaphase, WM-Gruppe)
    matchday: Mapped[Optional[int]]
    # Gruppenname der WM-Gruppenphase (z. B. "A", "Gruppe A")
    group_name: Mapped[Optional[str]]
    # ID aus der externen Datenquelle (fixture id)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Berlin")),
    )
