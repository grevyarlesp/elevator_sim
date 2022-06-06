
import logging

from app import main

def test_hello(test_app):
    response = test_app.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"hello" : "world"}

