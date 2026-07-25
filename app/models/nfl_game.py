from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class NflGame(Base):
    """Ein NFL-Spiel innerhalb einer Saison, Saisonphase und Woche."""

    __tablename__ = "nfl_games"

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[int] = mapped_column(index=True)
    # Saisonphase: "reg" (Regular Season) oder "post" (Playoffs)
    season_type: Mapped[str] = mapped_column(default="reg", index=True)
    week: Mapped[Optional[int]] = mapped_column(index=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("nfl_teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("nfl_teams.id"))
    kickoff_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]]
    home_score: Mapped[Optional[int]]
    away_score: Mapped[Optional[int]]
    # ID aus der externen Datenquelle (Tank01 gameID)
    external_id: Mapped[Optional[str]] = mapped_column(index=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Berlin")),
    )
