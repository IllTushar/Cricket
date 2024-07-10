from pydantic import BaseModel


class ODI(BaseModel):
    name: str
    odi_runs: int
