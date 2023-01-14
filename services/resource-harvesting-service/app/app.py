import schedule
import time
import requests
from fastapi import FastAPI
from . import config
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
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

# start
res = requests.get('http://192.168.0.3:5002/config/resources')
validaterules = res.json()



@app.get("/config")
async def res_harvesting(validaterules: dict, production, values):
    all_res = validaterules['levels']['production'].keys()
    if production.keys in all_res:
        return production.values + values
    raise Exception ("Production не соответствует конфигурации")    

schedule.every(1).hours.do(res_harvesting) 

#schedule.every(1).hours.at("00:00").do(res_harvesting)


while True:
    schedule.run_pending()
    time.sleep(1)