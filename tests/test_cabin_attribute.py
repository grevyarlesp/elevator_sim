import os
from threading import Thread, Lock
import time

import pytest

from app.cabin_attribute import CabinAttribute
from pytest_mock import MockerFixture

def increment(cabin_attribute: CabinAttribute, n):
  for _ in range(n):
    aux = cabin_attribute.get_vec()


def test_cabin_attribute_thread_safety(mocker):
  ITERATION = 10000


  # mocker.patch('app.cabin_attribute.CabinAttribute.__enter__')
  # mocker.patch('app.cabin_attribute.CabinAttribute.get_current_floor')
  cabin_attribute = CabinAttribute(0, 0)

  threads = [
      Thread(target=increment, args=(
          cabin_attribute,
          ITERATION,
      )) for _ in range(10)
  ]


  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()

  # print(cabin_attribute.vec)
  # assert cabin_attribute.vel == (ITERATION * len(threads))
