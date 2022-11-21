from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .schemas.building import Building, BuildingIn
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from . import crud, config
import typing
import logging
from fastapi.logger import logger

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
    return crud.create_building(db=db, building=building)
   


@app.get("/buildings", summary='Возвращает список построек', response_model=list[Building])
async def get_building_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
    ) -> typing.List[Building] :
    return crud.get_buildings(db, skip, limit)


@app.put("/buildings/{buildingId}", summary='Обновляет информацию о постройке')
async def update_building(buildingId: int, building: BuildingIn, db: Session = Depends(get_db)) -> Building :
    building = crud.update_building(db, buildingId, building)
    if building != None:
        return building
    return JSONResponse(status_code=404, content={"message": "Item not found"})



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