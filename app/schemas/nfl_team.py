from pydantic import BaseModel, ConfigDict


class NflTeamBase(BaseModel):
    name: str
    conference: str | None = None
    division: str | None = None
    abbreviation: str | None = None
    city: str | None = None
    logo_url: str | None = None
    external_id: int | None = None


class NflTeamCreate(NflTeamBase):
    pass


class NflTeamRead(NflTeamBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
