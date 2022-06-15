from app.cabin import Cabin
from app.config import get_settings
import pytest
from pytest_mock import MockerFixture
import time


def test_cabin_1(mocker):
  num_floors = 10
  tasks = [(5, 3), (2, 7), (4, 3), (1, 0), (5, 0)]

  cabin = Cabin(num_floors)
  cabin.start()

  for u, v in tasks:
    time.sleep(0.5)
    cabin.add_task(u, v)

  time.sleep(10)

  cabin.terminate()
