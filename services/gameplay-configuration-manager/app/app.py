from fastapi import FastAPI
from fastapi.responses import JSONResponse
from . import config
import json
from fastapi import FastAPI, Depends
import logging
from fastapi.logger import logger

app = FastAPI()

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


with open(cfg.config_path, 'r', encoding = 'utf-8') as f:
    config = json.load(f)


@app.get("/config/{config_path:path}", summary='')
async def read_config(config_path: str):
    try:
        fetch_data = extract_config(config, config_path.split("/"))
        return fetch_data
    except KeyError:
        return JSONResponse(status_code=404, content={"message": "Item not found"})


def extract_config(config_dict, hierarchy=[]):
        if len(hierarchy)==0:
            return config_dict
        else:
            key = hierarchy.pop(0)
            return extract_config(config_dict[key], hierarchy)
         
