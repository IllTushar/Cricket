from pydantic import BaseModel


class cricketer_profile(BaseModel):
    cricketer_name: str
    starting_year: int
    age: int
    country: str


class cricketer_profile_response(BaseModel):
    id: int
    cricketer_name: str
    starting_year: int
    age: int
    country: str

    class Config:
        orm_mode = True
