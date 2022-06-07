import logging 
import os 
from threading import Thread
from time import time

from app.task_tree import TaskTree

class Cabin(Thread):
    def __init__(self, num_floors : int):
        Thread.__init__(self)


        # TODO: set this up to have multiple ???
        self.currect_position = 1
        self.vec = -1 # 1 floor per second!
        self.target = -1

        self.Tasks = TaskTree()

    def get_compat_score(self, src_floor: int, dest_floor : int):

        pass

    def add_task(self):
        pass

    def get_status(self):
        pass

    def move_to(self, destination : int):
        pass

    def stop(self):
        pass

    def run(self):
        prev_floor = -1
        prev_time = 0
        while (True):
            pass
