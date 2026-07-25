from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class NflStanding(Base):
    """Bilanz eines NFL-Teams in einer Saison (W/L/D).

    Die Prozentquote (PCT) sowie Division-/Conference-/League-Ansichten
    werden aus diesen Werten bzw. den Team-Attributen abgeleitet.
    """

    __tablename__ = "nfl_standings"

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[int] = mapped_column(index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("nfl_teams.id"))
    wins: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    ties: Mapped[int] = mapped_column(default=0)
    # Rang innerhalb der Division (optional, falls von der Quelle geliefert)
    division_rank: Mapped[Optional[int]]
