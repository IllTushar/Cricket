from pydantic import BaseModel


class Rank_Create(BaseModel):
    ODI: int
    Test: int
    T20: int


class Ranks_Response(BaseModel):
    id: int
    player: str
    ODI: int
    Test: int
    T20: int

    class Config:
        orm_mode = True
