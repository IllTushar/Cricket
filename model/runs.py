from pydantic import BaseModel


class RunsRequest(BaseModel):
    odi_runs: int
    test_runs: int
    T20_runs: int


class Runs_Response(BaseModel):
    id: int
    player_id: int
    di_runs: int
    test_runs: int
    T20_runs: int

    class Config:
        orm_mode = True
