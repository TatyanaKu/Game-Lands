from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .schemas.resource_1 import Resource, ResourceIn
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from . import crud, config
import typing
import logging
from fastapi.logger import logger
import requests

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
res = requests.get('http://192.168.0.3:5002/config/resources')
validaterules = res.json()

app = FastAPI(
    version='0.0.1',
    title='Resource Service'
)
resources: typing.Dict[int, Resource] = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/resources", status_code=201, response_model=Resource,
    summary='Добавляет ресурс в базу'
)
async def add_resource(resource: ResourceIn, db: Session = Depends(get_db)) -> Resource :
    try: 
        check_resources(resource, validaterules)
    except Exception as exc:
        logger.error(exc)
        return JSONResponse(status_code=409, content={"message": "Resource does not exist"})
    return crud.create_resource(db=db, resource=resource)

def check_resources(resource: ResourceIn, validaterules: dict):
    all_types = validaterules['types'].keys()   
    if resource.type not in all_types:
        raise Exception ("Тип ресурса не существует в конфигурации")



@app.get("/resources", summary='Возвращает список ресурсов', response_model=list[Resource])
async def get_resource_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
    ) -> typing.List[Resource] :
    return crud.get_resources(db, skip, limit)


@app.put("/resources/{resourceId}", summary='Обновляет информацию о ресурсе')
async def update_resource(resourceId: int, resource: ResourceIn, db: Session = Depends(get_db)) -> Resource :
    resource = crud.update_resource(db, resourceId, resource)
    if resource != None:
        return resource
    return JSONResponse(status_code=404, content={"message": "Item not found"})



@app.delete("/resources/{resourceId}", summary='Удаляет ресурс из базы')
async def delete_resource(resourceId: int, db: Session = Depends(get_db)) -> Resource :
    if crud.delete_resource(db, resourceId):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get("/resources/{resourceId}", summary='Возвращает информацию о ресурсе')
async def get_resource_info(resourceId: int, db: Session = Depends(get_db)) -> Resource :
    resource = crud.get_resource(db, resourceId)
    if resource != None:
        return resource
    return JSONResponse(status_code=404, content={"message": "Item not found"})
