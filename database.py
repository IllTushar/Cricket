from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

BASE_URL = 'sqlite:///./cricket.db'

engin = create_engine(BASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engin)

Base = declarative_base()
