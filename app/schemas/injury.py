from datetime import date

from pydantic import BaseModel, ConfigDict


class InjuryBase(BaseModel):
    player_id: int
    team_id: int
    description: str | None = None
    since: date | None = None
    missed_matches: int | None = None
    status: str | None = None


class InjuryCreate(InjuryBase):
    pass


class InjuryRead(InjuryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class InjuryWithPlayer(BaseModel):
    """Verletzung mit eingebetteten Spielerinformationen für die API-Antwort."""

    id: int
    player_name: str
    position: str | None = None
    age: int | None = None
    description: str | None = None
    since: date | None = None
    missed_matches: int | None = None
    status: str | None = None
