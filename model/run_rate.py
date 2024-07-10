from pydantic import BaseModel


class RunRate(BaseModel):
    strike_rate: float


class RunRateResponse(BaseModel):
    id: int
    player_id: int
    strike_rate: float

    class Config:
        orm_mode = True
