from pydantic import BaseModel, ConfigDict


class DriverBase(BaseModel):
    name: str
    team: str | None = None
    number: int | None = None
    abbreviation: str | None = None
    country: str | None = None
    team_color: str | None = None
    external_id: int | None = None


class DriverCreate(DriverBase):
    pass


class DriverRead(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
