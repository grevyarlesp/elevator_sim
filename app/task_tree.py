import logging
from app.config import get_settings
from sortedcontainers import SortedSet

from threading import Lock


class TaskTree:
  """
  The task tree:
  Find the next floor with tasks in O(log n), with n is the number of floor
  Implemented to be thread safe
  """

  def __init__(self, num_floors: int = 10):
    """Floors : numbered from 1 to n
    """
    self.__num_floors = num_floors
    self.__tasks_sets = [set() for _ in range(num_floors + 1)]
    self.__tree = SortedSet()
    self._lock = Lock()

  def get_num_floors(self):
    """
    Get number of floors
    """
    with self._lock:
      return self.__num_floors

  def __mod_set(self, pos: int, val: int):
    """
    Modify the the task tree.
    """
    # DO not lock this! Other methods use this.
    if val > 0:
      self.__tree.add(pos)
    else:
      self.__tree.discard(pos)

  def check_tasks_current_floor(self, current_floor: int):
    """
    Check if there is a tasks in the current floor
    """
    with self._lock:
      if (current_floor < 1 or current_floor > self.__num_floors):
        return False
      return len(self.__tasks_sets[current_floor]) > 0

  def query_up(self, current_floor: int):
    """
    Find the closest floor higher than the current floor with a task
    """

    with self._lock:
      if (current_floor < 1 or current_floor > self.__num_floors):
        return -1

      index = self.__tree.bisect_left(current_floor)

      if index == len(self.__tree):
        return -1
      return self.__tree[index]

  def query_down(self, current_floor: int):
    """
    Find the closest floor lower than the current floor with a task
    """

    with self._lock:

      if (current_floor < 1 or current_floor > self.__num_floors):
        return -1

      index = self.__tree.bisect_left(current_floor)
      if index == 0:  # Nothing on the left
        return -1
      return self.__tree[index - 1]

  def add_task(self, floor: int, task: int):
    """Floor i has tasks with 2 type:
      = 0: Drop passenger at floor i
      > 0: Pick up passenger at floor i and move there.
    """

    with self._lock:
      if (floor < 1 or floor > self.__num_floors):
        logging.warning("Request invalid tasks! %d to %d", floor,
                        self.__num_floors)
        return False

      if (task < 0 or task > self.__num_floors):
        logging.warning("Request invalid tasks! %d to %d", floor,
                        self.__num_floors)
        return False

      if floor == task:
        return False

      self.__tasks_sets[floor].add(task)

      if get_settings().testing:
        print("Number of tasks", floor, len(self.__tasks_sets[floor]))

      num_tasks = len(self.__tasks_sets[floor])
      # print("Floor", floor, num_tasks)
      self.__mod_set(floor, num_tasks)
      return True

  def fullfill_all_tasks_on_floor(self, floor: int):
    """
    Fullfill all tasks for floor i
    """
    with self._lock:
      tasks_set = self.__tasks_sets

      b = False

      # get each task from the that floor to fullfill.
      while len(tasks_set[floor]) > 0:
        b = True
        next_floor = tasks_set[floor].pop()

        if next_floor == 0:
          continue

        tasks_set[next_floor].add(0)
        num_tasks = len(tasks_set[next_floor])

        self.__mod_set(next_floor, num_tasks)

      num_tasks = len(tasks_set[floor])
      self.__mod_set(floor, num_tasks)
      assert num_tasks == 0
      return b
