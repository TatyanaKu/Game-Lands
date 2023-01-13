from html import entities
from xml.dom.minidom import Entity
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .schemas.building import Building, BuildingIn
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from . import crud, config
import typing
import logging
from fastapi.logger import logger
import requests
import json


# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json(by_alias=True, indent=4)}'
)

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(cfg.postgres_dsn)


# start
res = requests.get('http://192.168.0.3:5003/config/buildings')
validaterules = res.json()


app = FastAPI(
    version='0.0.1',
    title='Building Service'
)
buildings: typing.Dict[int, Building] = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/buildings", status_code=201, response_model=Building,
    summary='Добавляет постройку в базу'
)
async def add_building(building: BuildingIn, db: Session = Depends(get_db)) -> Building :
    try: 
        check_buildings(building, validaterules)
    except Exception as exc:
        logger.error(exc)
        return JSONResponse(status_code=409, content={"message": "Building does not exist"})
    return crud.create_building(db=db, building=building)
    
def check_buildings(building: BuildingIn, validaterules: dict):
    all_types = validaterules['types'].keys()   
    if building.type not in all_types:
        raise Exception ("Тип здания не существует в конфигурации")
    if building.level != 0:
        raise Exception ("Уровень не соответствует конфигурации")

            

@app.get("/buildings", summary='Возвращает список построек', response_model=list[Building])
async def get_building_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
    ) -> typing.List[Building] :
    return crud.get_buildings(db, skip, limit)


@app.put("/buildings/{buildingId}", summary='Обновляет информацию о постройке')
async def update_building(buildingId: int, building: BuildingIn, db: Session = Depends(get_db)) -> Building :
    try:
        up_buildings(building, validaterules)
    except Exception as exc:
        logger.error(exc)
        return JSONResponse(status_code=409, content={"message": "Update not possible"})
    building = crud.update_building(db, buildingId, building)
    if building != None:
        return building

def up_buildings(building: BuildingIn, validaterules: dict):
    new_level = building.level + 1
    if new_level not in validaterules['levels']:
      raise Exception ("Уровень здания не соответствует")
    
    #building.level += 1
    # all_types = validaterules['types'].keys()
    # if building.level in building:
    #     return building.level + 1
    # raise Exception ("Уровень здания не соответствует") 


@app.delete("/buildings/{buildingId}", summary='Удаляет постройку из базы')
async def delete_building(buildingId: int, db: Session = Depends(get_db)) -> Building :
    if crud.delete_building(db, buildingId):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get("/buildings/{buildingId}", summary='Возвращает информацию о постройке')
async def get_building_info(buildingId: int, db: Session = Depends(get_db)) -> Building :
    building = crud.get_building(db, buildingId)
    if building != None:
        return building
    return JSONResponse(status_code=404, content={"message": "Item not found"})