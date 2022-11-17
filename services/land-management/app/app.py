from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .schemas.land import Land, LandIn
from sqlalchemy.orm import Session
from .schemas.command import Command, Scene
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
    title='Land Service'
)
lands: typing.Dict[int, Land] = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/lands", status_code=201, response_model=Land,
    summary='Добавляет землю в базу'
)
async def add_land(land: LandIn, db: Session = Depends(get_db)) -> Land :
    return crud.create_land(db=db, land=land)


@app.get("/lands", summary='Возвращает список земель', response_model=list[Land])
async def get_land_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
    ) -> typing.List[Land] :
    return crud.get_lands(db, skip, limit)


@app.put("/lands/{landId}", summary='Обновляет информацию о земле')
async def update_land(landId: int, land: LandIn, db: Session = Depends(get_db)) -> Land :
    land = crud.update_land(db, landId, land)
    if land != None:
        return land
    return JSONResponse(status_code=404, content={"message": "Item not found"})



@app.delete("/lands/{landId}", summary='Удаляет землю из базы')
async def delete_land(landId: int, db: Session = Depends(get_db)) -> Land :
    if crud.delete_land(db, landId):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get("/lands/{landId}", summary='Возвращает информацию о земле')
async def get_land_info(landId: int, db: Session = Depends(get_db)) -> Land :
    land = crud.get_land(db, landId)
    if land != None:
        return land
    return JSONResponse(status_code=404, content={"message": "Item not found"})

