from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Standing(Base):
    """Tabellenplatz eines Teams in einem Fußball-Wettbewerb.

    Deckt sowohl Ligatabellen (Bundesliga, CL-Ligaphase) als auch
    Gruppentabellen (WM-Gruppenphase) ab. Für Gruppentabellen ist
    ``group_name`` gesetzt, für reine Ligatabellen bleibt es leer.
    """

    __tablename__ = "standings"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"), index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    # Gruppenname bei Gruppenphasen (z. B. "A"), sonst NULL
    group_name: Mapped[Optional[str]] = mapped_column(index=True)
    rank: Mapped[Optional[int]]
    played: Mapped[int] = mapped_column(default=0)
    won: Mapped[int] = mapped_column(default=0)
    draw: Mapped[int] = mapped_column(default=0)
    lost: Mapped[int] = mapped_column(default=0)
    goals_for: Mapped[int] = mapped_column(default=0)
    goals_against: Mapped[int] = mapped_column(default=0)
    goal_difference: Mapped[int] = mapped_column(default=0)
    points: Mapped[int] = mapped_column(default=0)
