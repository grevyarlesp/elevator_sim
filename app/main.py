from fastapi import FastAPI, Path
import logging
from app.config import get_settings
from app.scheduler import Scheduler

app = FastAPI()
user = 0

log = logging.getLogger("uvicorn")
scheduler = Scheduler(get_settings().num_floors, get_settings().num_cabins)


@app.on_event("startup")
async def startup_event():
  log.info("Starting the elevators...")
  scheduler.start_cabins()


@app.get("/")
async def get_settings_app():
  return {
      "Testing": get_settings().testing,
      "num_cabins": get_settings().num_cabins,
      "num_floors": get_settings().num_floors,
      "output_log": get_settings().output_log
  }


@app.get("/about")
async def get_about():
  return {"info": "Elevator app by quoctk2"}


@app.get("/cabin/{id}")
async def get_current_floor(id: int):
  return 0


@app.post("/move/{src_floor},{dest_floor}")
async def post_request(src_floor: int = Path(title="From floor",
                                             ge=1,
                                             le=get_settings().num_floors,
                                             default=-1),
                       dest_floor: int = Path(title="From floor",
                                              ge=1,
                                              le=get_settings().num_floors,
                                              default=-1)):
  if src_floor == -1 or dest_floor == -1:
    return
  global scheduler
  scheduler.process_request(src_floor, dest_floor)
  return 0
