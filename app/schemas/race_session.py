from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RaceSessionBase(BaseModel):
    race_id: int
    name: str
    session_type: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None
    external_id: int | None = None


class RaceSessionCreate(RaceSessionBase):
    pass


class RaceSessionRead(RaceSessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
