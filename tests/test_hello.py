import logging

from app import main


def test_hello(test_app):
  response = test_app.get("/about")
  assert response.status_code == 200
  assert response.json() ==  {"info": "Elevator app by quoctk2"}
