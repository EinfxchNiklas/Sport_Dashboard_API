from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Player(Base):
    """Fußballspieler eines Teams (für die Verletzten-Übersicht)."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # Position im Klartext (z. B. "Innenverteidiger")
    position: Mapped[Optional[str]]
    age: Mapped[Optional[int]]
    number: Mapped[Optional[int]]
    nationality: Mapped[Optional[str]]
    # ID aus der externen Datenquelle
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
