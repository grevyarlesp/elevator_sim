import logging
import os
from threading import Thread, Lock
from time import time

from app.config import get_settings
from app.cabin import Cabin

log = logging.getLogger("uvicorn")


class Scheduler:
  """
  The scheduler for the elevators.
  """

  def __init__(self, num_floors: int, num_cabins: int):
    self.num_floors = num_floors
    self.num_cabins = num_cabins
    self.next = 0
    self.cabins = [Cabin(self.num_floors) for _ in range(self.num_cabins)]
  def start_cabins(self):
    for cabin in self.cabins:
      cabin.start()

  def process_request(self, src_floor: int, dest_floor: int):
    self.cabins[self.next].add_task(src_floor, dest_floor)
    if get_settings().output_log:
      log.info("(%d, %d) assigned to cabin %s,", src_floor, dest_floor,
               self.cabins[self.next].name)

    self.next = (self.next + 1) % self.num_floors

  def __del__(self):
    for cabin in self.cabins:
      cabin.terminate()