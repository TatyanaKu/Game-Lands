from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .schemas.land import Land
import typing


app = FastAPI(
    version='0.0.1',
    title='Land Service'
)
lands: typing.Dict[int, Land] = {}

@app.post(
    "/lands", status_code=201, response_model=Land,
    summary='Добавляет землю игроку'
)
async def add_land(land: Land) -> Land:
    if land.id in lands:
        return JSONResponse(status_code=409, content={"message": "Conflict"})
    lands[land.id] = land
    return land


@app.get("/lands", summary='Возвращает список земель', response_model=list[Land])
async def get_land_list() -> typing.Iterable[Land] :
    return [ v for k,v in lands.items() ]


@app.put("/lands/{landId}", summary='Обновляет информацию о земле')
async def update_land(landId: int, land: Land) -> Land :
    if landId not in lands:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    lands[landId] = land
    return lands[landId]


@app.delete("/lands/{landId}", summary='Удаляет землю из базы')
async def delete_land(landId: int) -> Land :
    if landId in lands:
        del lands[landId]
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get("/lands/{landId}", summary='Возвращает информацию о земле')
async def get_land_info(landId: int) -> Land :
    if landId in lands: 
        return lands[landId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})
