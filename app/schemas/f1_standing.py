from pydantic import BaseModel, ConfigDict


class DriverStandingBase(BaseModel):
    season: str
    driver_id: int
    position: int | None = None
    points: float = 0
    wins: int = 0


class DriverStandingCreate(DriverStandingBase):
    pass


class DriverStandingRead(DriverStandingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ConstructorStandingBase(BaseModel):
    season: str
    team: str
    team_color: str | None = None
    position: int | None = None
    points: float = 0
    wins: int = 0


class ConstructorStandingCreate(ConstructorStandingBase):
    pass


class ConstructorStandingRead(ConstructorStandingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
