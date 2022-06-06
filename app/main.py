from fastapi import FastAPI
from app.task_tree import TaskTree

app = FastAPI()
user = 0

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

tasktree = TaskTree(num_floors = 100)
# from floor 1 to floor 10
tasktree.add_task(1, 10)
print(tasktree.__num_floors)
