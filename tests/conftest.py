# project/tests/conftest.py

import os

import pytest
from starlette.testclient import TestClient

from app import main
from app.config import get_settings, Settings

from app.cabin import Cabin


import logging

def get_settings_override():
  return Settings(testing=1)


@pytest.fixture(scope="module")
def test_app():

  logging.info("Enter testing...")
  # set up
  # override pytest dependency
  main.app.dependency_overrides[get_settings] = get_settings_override
  with TestClient(main.app) as test_client:
    # testing
    yield test_client
  # tear down


@pytest.fixture(autouse=True)
def dummy_cabin():
  # setup
  main.app.dependency_overrides[get_settings] = get_settings_override
