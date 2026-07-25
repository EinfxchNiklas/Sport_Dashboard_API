from pydantic import BaseModel, ConfigDict


class StandingBase(BaseModel):
    competition_id: int
    team_id: int
    group_name: str | None = None
    rank: int | None = None
    played: int = 0
    won: int = 0
    draw: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    goal_difference: int = 0
    points: int = 0


class StandingCreate(StandingBase):
    pass


class StandingRead(StandingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
