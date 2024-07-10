from pydantic import BaseModel


class StrikeRateResponse(BaseModel):
    name: str
    strike_rate: float
