from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RaceSession(Base):
    """Einzelne Session eines Rennwochenendes.

    Ein Rennwochenende (``Race``) besteht aus mehreren Sessions wie
    Practice 1/2/3, Sprint Qualifying, Sprint, Qualifying und Race.
    """

    __tablename__ = "race_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id"), index=True)
    # Anzeigename (z. B. "Practice 1", "Qualifying", "Race")
    name: Mapped[str] = mapped_column(nullable=False)
    # Technischer Typ: "practice" | "sprint_qualifying" | "sprint"
    # | "qualifying" | "race"
    session_type: Mapped[Optional[str]] = mapped_column(index=True)
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    # Geplantes / tatsächliches Ende der Session (aus OpenF1 date_end)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]]
    # ID aus der externen Datenquelle (OpenF1 session_key)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
