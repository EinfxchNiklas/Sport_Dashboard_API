from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RaceBase(BaseModel):
    season: str | None = None
    name: str
    date: datetime | None = None
    status: str | None = None
    location: str | None = None
    country: str | None = None
    round: int | None = None
    external_id: int | None = None


class RaceCreate(RaceBase):
    pass


class RaceRead(RaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
