from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MatchBase(BaseModel):
    competition_id: int
    home_team_id: int
    away_team_id: int
    kickoff_time: datetime | None = None
    status: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    stage: str | None = None
    round_name: str | None = None
    matchday: int | None = None
    group_name: str | None = None
    external_id: int | None = None


class MatchCreate(MatchBase):
    pass


class MatchRead(MatchBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime | None = None
