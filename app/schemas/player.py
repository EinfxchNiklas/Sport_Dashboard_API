from pydantic import BaseModel, ConfigDict


class PlayerBase(BaseModel):
    team_id: int
    name: str
    position: str | None = None
    age: int | None = None
    number: int | None = None
    nationality: str | None = None
    external_id: int | None = None


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
