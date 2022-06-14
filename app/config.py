import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")

class Settings(BaseSettings):
  environment: str = os.getenv("ENVIRONMENT", "dev")
  testing: int = os.getenv("TESTING", 0)
  output_log: bool = os.getenv("OUTPUT_LOG", True)

  num_cabins: int = os.getenv("NUM_CABINS", 10)
  num_floors: int = os.getenv("NUM_FLOORS", 10)
  cabin_time: int = os.getenv("CABIN_TIME", 1000)


@lru_cache()
def get_settings() -> Settings:
  log.info("Loading config settings from the environment...")
  return Settings()
