from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DriverStanding(Base):
    """Stand der Fahrer-Weltmeisterschaft für eine Saison."""

    __tablename__ = "driver_standings"

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[str] = mapped_column(index=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    position: Mapped[Optional[int]]
    points: Mapped[float] = mapped_column(default=0)
    wins: Mapped[int] = mapped_column(default=0)


class ConstructorStanding(Base):
    """Stand der Konstrukteurs-Weltmeisterschaft für eine Saison."""

    __tablename__ = "constructor_standings"

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[str] = mapped_column(index=True)
    # Team-/Konstrukteursname (F1-Teams werden nicht als eigene Tabelle geführt)
    team: Mapped[str] = mapped_column(nullable=False)
    team_color: Mapped[Optional[str]]
    position: Mapped[Optional[int]]
    points: Mapped[float] = mapped_column(default=0)
    wins: Mapped[int] = mapped_column(default=0)
