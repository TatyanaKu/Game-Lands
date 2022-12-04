from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os


app = FastAPI()

with open('config.json', 'r', encoding = 'utf-8') as f:
    lands, buildings, resourses = json.load(f)

@app.get("/config/{config_path:path}", summary='')
async def read_config(config_path: str):
    if config_path != None:
        print(config_path.split("/"))
        return {"config_path": config_path}
    return JSONResponse(status_code=404, content={"message": "Item not found"})


#рекурсивная функция извлечет из конфига нужный кусок


