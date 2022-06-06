from fastapi import FastAPI
from app.task_tree import TaskTree

app = FastAPI()
user = 0

@app.get("/hello")
async def getHello() -> str:
    return { "hello": "world"}

def check():
    global user
    while (user < 3):
        # print(user)
        pass

@app.post("/{id}")
def getUser(id):
    global user
    user += 1
    check()
    return user



