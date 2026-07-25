from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class NflTeam(Base):
    __tablename__ = "nfl_teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    conference: Mapped[Optional[str]]
    division: Mapped[Optional[str]]
    # Kürzel (z. B. "ARI", "KC")
    abbreviation: Mapped[Optional[str]] = mapped_column(index=True)
    city: Mapped[Optional[str]]
    logo_url: Mapped[Optional[str]]
    # ID aus der externen Datenquelle (Tank01 teamID)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
