from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    name: str
    short_name: str | None = None
    country: str | None = None
    logo_url: str | None = None
    external_id: int | None = None


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
