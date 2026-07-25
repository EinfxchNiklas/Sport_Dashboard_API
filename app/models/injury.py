from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Injury(Base):
    """Verletzung eines Spielers (Verletzten-Tab auf der Team-Seite)."""

    __tablename__ = "injuries"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    # Art der Verletzung (z. B. "Kreuzbandriss")
    description: Mapped[Optional[str]]
    # Verletzt seit
    since: Mapped[Optional[date]] = mapped_column(Date)
    # Anzahl verpasster Spiele
    missed_matches: Mapped[Optional[int]]
    # Status (z. B. "out", "doubtful")
    status: Mapped[Optional[str]]
