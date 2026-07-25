from pydantic import BaseModel, ConfigDict


class CompetitionBase(BaseModel):
    name: str
    sport: str
    country: str | None = None
    season: str | None = None
    slug: str | None = None
    format: str | None = None
    logo_url: str | None = None
    external_id: int | None = None


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionRead(CompetitionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
