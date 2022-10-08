from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .schemas.land import Land, LandBase
from .schemas.command import Command, Scene
import typing

FAKE_LAND_INFO =  {}

app = FastAPI(
    version='0.0.1',
    title='Land Service'
)
lands: typing.Dict[int, Land] = {}

@app.post(
    "/lands", status_code=201, response_model=Land,
    summary='Добавляет землю игроку'
)
async def add_land(land: LandBase) -> Land:
    result = Land(
        **land.dict(),
        id=len(lands) + 1,
        info=FAKE_LAND_INFO
    )
    lands[result.id] = result
    return result

@app.get("/lands", summary='Возвращает список земель', response_model=list[Land])
async def get_land_list() -> typing.Iterable[Land] :
    return [ v for k,v in lands.items() ]


@app.put("/lands/{landId}", summary='Обновляет информацию о земле')
async def update_land(landId: int, land: LandBase) -> Land :
    if landId in lands:
        result = Land(
            **land.dict(),
            id=landId,
            info=FAKE_LAND_INFO
        )
        lands[landId] = result
        return lands[landId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete("/lands/{landId}", summary='Удаляет землю из базы')
async def delete_land(landId: int) -> Land :
    if landId in lands:
        del lands[landId]
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.get("/lands/{landId}/fetch", summary='Инициирует запрос актуальной информации о земле')
async def fetch_land_data(landId: int) -> Land :
    if landId in lands: return lands[landId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})


