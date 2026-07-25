from pydantic import BaseModel, ConfigDict, computed_field


class NflStandingBase(BaseModel):
    season: int
    team_id: int
    wins: int = 0
    losses: int = 0
    ties: int = 0
    division_rank: int | None = None


class NflStandingCreate(NflStandingBase):
    pass


class NflStandingRead(NflStandingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class NflStandingWithTeam(BaseModel):
    """NFL-Standing mit eingebetteten Team-Infos und berechnetem PCT-Wert."""

    id: int
    season: int
    team_name: str
    team_abbreviation: str | None = None
    conference: str | None = None
    division: str | None = None
    wins: int
    losses: int
    ties: int
    division_rank: int | None = None

    @computed_field
    @property
    def pct(self) -> float:
        total = self.wins + self.losses + self.ties
        return round(self.wins / total, 3) if total > 0 else 0.0
