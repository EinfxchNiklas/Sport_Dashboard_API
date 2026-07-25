from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    team: Mapped[Optional[str]]
    number: Mapped[Optional[int]]
    # Kürzel (z. B. "VER", "HAM")
    abbreviation: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    # Teamfarbe als Hex-Wert für die Darstellung
    team_color: Mapped[Optional[str]]
    # ID aus der externen Datenquelle (OpenF1 driver_number / driver id)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
