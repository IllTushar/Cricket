from database import Base
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, Float
from sqlalchemy.orm import relationship


# Profile
class CricketerProfile(Base):
    __tablename__ = 'Profile'
    id = Column(Integer, autoincrement=True, primary_key=True)
    cricketer_name = Column(String, nullable=False)
    starting_year = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    rank = relationship('Ranking', back_populates='profile')
    run_rate = relationship('RunRateTable', back_populates='profile')
    run_table = relationship('Runs', back_populates='runs')


class Ranking(Base):
    __tablename__ = 'Ranks'
    id = Column(Integer, autoincrement=True, primary_key=True)
    player = Column(String, ForeignKey('Profile.id'), nullable=False)
    ODI = Column(String, nullable=False)
    Test = Column(String, nullable=False)
    T20 = Column(String, nullable=False)
    profile = relationship('CricketerProfile', back_populates='rank')


class RunRateTable(Base):
    __tablename__ = 'RunRate'
    id = Column(Integer, autoincrement=True, primary_key=True)
    player_id = Column(Integer, ForeignKey("Profile.id"), nullable=False)
    strike_rate = Column(Float, nullable=False)
    profile = relationship('CricketerProfile', back_populates='run_rate')


class Runs(Base):
    __tablename__ = 'Total Run'
    id = Column(Integer, autoincrement=True, primary_key=True)
    player_id = Column(Integer, ForeignKey('Profile.id'), nullable=False)
    odi_runs = Column(Integer, nullable=False)
    test_runs = Column(Integer, nullable=False)
    T20_runs = Column(Integer, nullable=False)
    runs = relationship('CricketerProfile', back_populates='run_table')
