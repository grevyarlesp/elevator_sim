from fastapi import FastAPI
from app.task_tree import TaskTree
from app.config import get_settings

app = FastAPI()
user = 0

@app.get("/")
async def getSettings():
    return {
            "Testing" : get_settings().testing, 
            "num_cabins" : get_settings().num_cabins, 
            "num_floors" : get_settings().num_floors
            }


@app.get("/hello")
async def getHello() -> str:
    return { "hello": "world"}

@app.post("/{id}")
def postUser(id):
    global user
    user += 1
    return user

@app.post("/{src_floor}/{dest_floor}")
def postRequest(src_floor : int, dest_floor : int):
    pass


