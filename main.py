from fastapi import FastAPI

from database import engin
from table.table import Base
from router import create_user

app = FastAPI()


# Base.metadata.drop_all(bind=engin)
Base.metadata.create_all(bind=engin)
app.include_router(create_user.router)
