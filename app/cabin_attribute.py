from app.config import get_settings

from threading import Lock


class CabinAttribute:
  """Attributes for the cabin
  Implemented to be thread safe
  Wrap attributes that need to access multiple threads
  """

  def __init__(self, current_floor: int, num_floors: int):

    self._lock = Lock()

    self.current_floor: int = current_floor
    self.vel: int = 0
    self.target: int = -1

    # Number of floors
    self.num_floors = num_floors

  def set_target_and_move(self, target: int):
    """
    For the elevator, set the target and move to it.
    """
    with self._lock:
      if target == self.current_floor:
        # Do nothing
        return
      self.target = target
      if self.current_floor < self.target:
        self.vel = 1
      else:
        self.vel = -1

  def move(self):
    with self._lock:
      if (self.vel + self.current_floor > 0 and
          self.vel + self.current_floor <= self.num_floors):
        self.current_floor += self.vel

  def pause(self):
    """Pausing the elevator, set velocity to 0.
    Set it on standy
    """
    with self._lock:
      self.vel = 0
      self.target = -1

  def is_paused(self):
    with self._lock:
      return self.vel == 0

  # DO NOT USE THESE WITH THIS CLASS!
  def reached_target(self):
    with self._lock:
      return self.target == self.current_floor

  def get_current_floor(self):
    with self._lock:
      return self.current_floor

  def set_current_floor(self, value: int):
    with self._lock:
      self.vel = value

  def get_vec(self):
    with self._lock:
      return self.vel

  def get_target(self):
    with self._lock:
      return self.target
