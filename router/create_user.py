from fastapi import APIRouter, Depends, status, HTTPException
from database import SessionLocal
from model.profile import cricketer_profile, cricketer_profile_response
from model.ranking import Rank_Create, Ranks_Response
from model.run_rate import RunRate
from typing import List
from model.strike_rate.strike_rate_model import StrikeRateResponse
from model.runs import RunsRequest, Runs_Response
from model.runing.odi import ODI
from sqlalchemy.orm import Session
from table.table import CricketerProfile
from table.table import Ranking, RunRateTable, Runs

router = APIRouter()


# Connect DB
def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Cricketer Profile
@router.post('/create-new_cricketer', status_code=status.HTTP_201_CREATED)
def create_new_cricketer(request_body: cricketer_profile, db: Session = Depends(connect_db)):
    new_data = CricketerProfile(**request_body.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.get('/country_players/{country_name}', status_code=status.HTTP_200_OK)
def get_country_players(country_name: str, db: Session = Depends(connect_db)):
    get_players = db.query(CricketerProfile).filter(CricketerProfile.country == country_name.upper()).all()
    if get_players:
        return get_players
    else:
        raise HTTPException(status_code=404, detail="Not Found!!")


@router.post("/ranking/{player}", status_code=status.HTTP_201_CREATED)
def create_ranking(player_id: int, request: Rank_Create, db: Session = Depends(connect_db)):
    player_profile = db.query(CricketerProfile).filter(CricketerProfile.id == player_id).first()

    if player_profile:
        new_data = Ranking(player=player_id, **request.dict())
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data
    else:
        raise HTTPException(status_code=404, detail="Not found!!")


@router.get("/top-odi/{ranking}", status_code=status.HTTP_200_OK, response_model=List[str])
def get_top_odi(ranking: int, db: Session = Depends(connect_db)):
    # Fetch players with the given ODI ranking
    players = db.query(Ranking).filter(Ranking.ODI == ranking).all()

    if not players:
        raise HTTPException(status_code=404, detail="Not found")

    # Fetch player profiles for these players
    player_profiles = []
    for player in players:
        player_profile = db.query(CricketerProfile).filter(CricketerProfile.id == player.player).first()
        if player_profile:
            player_profiles.append(player_profile.cricketer_name)
        else:
            raise HTTPException(status_code=404, detail=f"Profile for player with ID {player.player_id} not found")

    return player_profiles


@router.post('/runrate/{player_id}', status_code=status.HTTP_201_CREATED)
def post_run_rate(player_id: int, request: RunRate, db: Session = Depends(connect_db)):
    player = db.query(CricketerProfile).filter(CricketerProfile.id == player_id).first()

    if player:
        run_rate = RunRateTable(player_id=player_id, **request.dict())
        db.add(run_rate)
        db.commit()
        db.refresh(run_rate)
        return run_rate
    else:
        raise HTTPException(status_code=404, detail="Player not found")


@router.get("/strike_rate/{strike_rate}", status_code=status.HTTP_200_OK, response_model=List[StrikeRateResponse])
def get_player_according_strike_rate(strike_rate: int, db: Session = Depends(connect_db)):
    if strike_rate <= 200:
        raise HTTPException(status_code=404, detail="find only those strike rates which is above 150")

    players = db.query(RunRateTable).filter(RunRateTable.strike_rate >= 200).all()

    if not players:
        raise HTTPException(status_code=404, detail="Not Found!!")

    # Fetch Players
    players_name_list: List[StrikeRateResponse] = []
    for player in players:
        player_name = db.query(CricketerProfile).filter(CricketerProfile.id == player.player_id).first()
        if player_name:
            players_name_list.append(
                StrikeRateResponse(name=player_name.cricketer_name, strike_rate=player.strike_rate))
        else:
            raise HTTPException(status_code=404, detail=f"Profile for player with ID {player.player_id} not found")

    return players_name_list


@router.delete("/delete_strike_rate/{id}", status_code=status.HTTP_200_OK)
def delete_strike_rate_data(id: int, db: Session = Depends(connect_db)):
    data = db.query(RunRateTable).filter(RunRateTable.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Deletion Successful", "data": data}


@router.post("/run/{player_id}", status_code=status.HTTP_201_CREATED)
def create_player(player_id: int, request: RunsRequest, db: Session = Depends(connect_db)):
    player_runs = db.query(CricketerProfile).filter(CricketerProfile.id == player_id).first()
    if player_runs:
        data_create_run_table = Runs(player_id=player_id, **request.dict())
        db.add(data_create_run_table)
        db.commit()
        db.refresh(data_create_run_table)
        return data_create_run_table
    else:
        raise HTTPException(status_code=404, detail="Player is not found!!")


@router.get('/highest_odi/{runing}', status_code=status.HTTP_200_OK, response_model=List[ODI])
def highest_odi(runs: int, db: Session = Depends(connect_db)):
    runs = db.query(Runs).filter(Runs.odi_runs >= runs).all()

    if runs:
        player_list: List[ODI] = []
        for run in runs:
            player = db.query(CricketerProfile).filter(CricketerProfile.id == run.player_id).first()
            if player:
                player_list.append(ODI(name=player.cricketer_name, odi_runs=run.odi_runs))

        return player_list
    else:
        raise HTTPException(status_code=404, detail="Details is not found")
