from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    short_name: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    logo_url: Mapped[Optional[str]]
    # ID aus der externen Datenquelle (API-Football team id, wird in den Website-URLs
    # als ?team=<external_id> verwendet)
    external_id: Mapped[Optional[int]] = mapped_column(index=True)
