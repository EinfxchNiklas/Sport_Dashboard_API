from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    sport: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[Optional[str]]
    season: Mapped[Optional[str]]
    # URL-Slug der Website (z. B. "wm", "champions-league", "dfb-pokal", "bundesliga")
    slug: Mapped[Optional[str]] = mapped_column(index=True)
    # Format des Wettbewerbs: "league", "cup", "tournament"
    format: Mapped[Optional[str]]
    logo_url: Mapped[Optional[str]]
    # ID aus der externen Datenquelle (z. B. API-Football league id)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
