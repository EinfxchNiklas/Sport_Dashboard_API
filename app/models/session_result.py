from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SessionResult(Base):
    """Ergebnis eines Fahrers in einer einzelnen Session."""

    __tablename__ = "session_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("race_sessions.id"), index=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    position: Mapped[Optional[int]]
    # Beste Zeit bzw. Gesamtzeit als Text (z. B. "1:29.842", "+5.321")
    time: Mapped[Optional[str]]
    laps: Mapped[Optional[int]]
    points: Mapped[Optional[float]]
    # Status (z. B. "Finished", "DNF", "DSQ")
    status: Mapped[Optional[str]]
