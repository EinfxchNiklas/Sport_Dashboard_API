from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NflGameBase(BaseModel):
    season: int
    season_type: str = "reg"
    week: int | None = None
    home_team_id: int
    away_team_id: int
    kickoff_time: datetime | None = None
    status: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    external_id: str | None = None


class NflGameCreate(NflGameBase):
    pass


class NflGameRead(NflGameBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime | None = None
