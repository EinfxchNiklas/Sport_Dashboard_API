from pydantic import BaseModel, ConfigDict


class SessionResultBase(BaseModel):
    session_id: int
    driver_id: int
    position: int | None = None
    time: str | None = None
    laps: int | None = None
    points: float | None = None
    status: str | None = None


class SessionResultCreate(SessionResultBase):
    pass


class SessionResultRead(SessionResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
