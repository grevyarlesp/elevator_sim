import logging
import os
from threading import Thread, Lock
import time
from app import cabin_attribute

from app.task_tree import TaskTree
from app.config import get_settings
from app.cabin_attribute import CabinAttribute

import pdb

log = logging.getLogger("uvicorn")


class Cabin(Thread):
  """Cabin class, implemented with a thread
  """

  def __init__(self, num_floors: int):
    Thread.__init__(self)

    self.num_floors = num_floors

    self.cabin_attribute = CabinAttribute(1, num_floors)
    self.task_tree = TaskTree()
    self._running = True

  def add_task(self, src_floor: int, task: int):
    self.task_tree.add_task(src_floor, task)

  def fullfill_tasks_on_floor(self, floor):
    self.task_tree.fullfill_all_tasks_on_floor(floor)

  def get_next_task(self, cabin_dir):
    if cabin_dir > 0:  # going up
      return self.task_tree.query_up(self.cabin_attribute.get_current_floor())
    else:  # going down
      return self.task_tree.query_down(self.cabin_attribute.get_current_floor())

  def stop(self):
    """
      Stop the elevator
      """

    # Move this to the loop!
    if get_settings().output_log:
      log.info("Stopping elevator %s at %d", self.name,
               self.cabin_attribute.get_current_floor())

    self.vec = 0
    self.target = -1

  def run(self):

    if get_settings().output_log:
      log.info("Cabin %s starts at %d", self.name,
               self.cabin_attribute.get_current_floor())
    self.fullfill_tasks_on_floor(self.cabin_attribute.get_current_floor())

    # breakpoint()

    # if task found previously
    prev_task = False

    while self._running:

      if not self.cabin_attribute.is_paused():

        if get_settings().output_log:
          log.info("Cabin %s: at %d", self.name,
                   self.cabin_attribute.get_current_floor())

        self.cabin_attribute.move()
        time.sleep(get_settings().cabin_time / 1000.0)

        self.fullfill_tasks_on_floor(self.cabin_attribute.get_current_floor())

      # Pause if reached target
      if self.cabin_attribute.reached_target():
        self.cabin_attribute.pause()

      if self.cabin_attribute.is_paused():
        # up first
        next_task = self.get_next_task(1)
        if next_task == -1:
          next_task = self.get_next_task(0)
        if next_task != -1:
          self.cabin_attribute.set_target_and_move(next_task)

        if get_settings().output_log:
          if next_task != -1:
            log.info("Cabin %s: Task found at %d", self.name, next_task)
            prev_task = True
          elif prev_task:
            prev_task = False
            log.info("Cabin %s: Found no task, continue sleeping...", self.name)

  def terminate(self):
    self._running = False
