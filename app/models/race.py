from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Race(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[Optional[str]]
    name: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]]
    # Austragungsort / Strecke (z. B. "Zandvoort")
    location: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    # Lauf-Nummer innerhalb der Saison
    round: Mapped[Optional[int]]
    # ID aus der externen Datenquelle (OpenF1 meeting_key)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
