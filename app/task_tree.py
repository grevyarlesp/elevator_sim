"""
The task tree: 
Find the next floor with tasks in O(log n), with n is the number of floor
"""

import logging
from app.config import get_settings
import pdb
from sortedcontainers import SortedSet

class TaskTree:
    def __init__(self, num_floors : int = 10):
        """ 
        Floors : numbered from 1 to n
        """
        self.__num_floors = num_floors
        self.__tasks_sets = [set() for _ in range(num_floors + 1)]
        self.__tree = SortedSet()

    def get_num_floors(self):
        """
        Get number of floors
        """
        return self.__num_floors

    def __mod_tree(self, pos : int, val : int):
        """ 
        Modify the the task tree.
        """
        if (val > 0):
            self.__tree.add(pos)
        else:
            self.__tree.discard(pos)

    def check_tasks_current_floor(self, current_floor : int):
        """
        Check if there is a tasks in the current floor
        """
        pass

    def query_up(self, current_floor : int):
        """ 
        Find the closest floor higher than the current floor with a task 
        """
        index = self.__tree.bisect_left(current_floor)
        if (index == len(self.__tree)):
            return -1
        return self.__tree[index]

    def query_down(self, current_floor : int):
        """ 
        Find the closest floor lower than the current floor with a task
        """
        index = self.__tree.bisect_left(current_floor)
        if (index == 0): # Nothing on the left
            return -1
        return self.__tree[index - 1]

    def add_task(self, floor: int, task : int):
        """
        Floor i has tasks with 2 type:
        = 0: Drop passenger at floor i
        > 0: Pick up passenger at floor i and move there.
        """

        if (floor < 1 or floor > self.__num_floors):
            logging.warning("Request invalid floor!" + " " + str(floor) + " " + str(self.__num_floors))
            return False

        if (task < 0 or task > self.__num_floors):
            logging.warning("Request invalid tasks!" + " " + str(floor) + " " + str(self.__num_floors))
            return False

        # Noone is going to the same floor!!!!
        if (floor == task):
            return False

        self.__tasks_sets[floor].add(task)

        if (get_settings().testing):
            print("Number of tasks", floor, len(self.__tasks_sets[floor]))

        num_tasks = len(self.__tasks_sets[floor])
        # print("Floor", floor, num_tasks)
        self.__mod_tree(floor, num_tasks)
        return True

    def fullfill_all_tasks_on_floor(self, floor : int):
        """
        Fullfill all tasks for floor i
        """
        __tasks_sets = self.__tasks_sets

        # get each task from the that floor to full fill.
        while (len(__tasks_sets[floor]) > 0):
            next_floor = __tasks_sets[floor].pop()
            # Move to ... 
            if (next_floor > 0):
                __tasks_sets[next_floor].add(0)
                num_tasks = len(__tasks_sets[next_floor])
                self.__mod_tree(next_floor, num_tasks)

        # Should be 0 -> mock test this? 
        num_tasks = len(__tasks_sets[floor])

        self.__mod_tree(floor, num_tasks)
