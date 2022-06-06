"""
The task tree: 
Find the next floor with tasks in O(log n), with n is the number of floor
"""

import logging

from app.config import get_settings

class TaskTree:
    def __init__(self, num_floors : int = 10):
        """ 
        Floors : numbered from 1 to n
        """
        self.__num_floors = num_floors
        self.__tasks_sets = [set() for _ in range(num_floors + 1)]
        self.__tree = [0] * 4 * (num_floors + 1)

    def get_num_floors(self):
        return self.__num_floors

    def __mod_tree(self, id : int, left : int, right: int, pos : int, val : int):
        """ 
        Modify the segment tree.
        Assign val to the position pos.
        """
        if (pos < left or pos > right):
            return
        if (pos == left and pos == right):
            self.__tree[id] = val
            return

        mid = (left + right) // 2
        self.__mod_tree(id * 2, left, mid, pos, val);
        self.__mod_tree(id * 2 + 1, mid + 1, right, pos, val);
        self.__tree[id]  = self.__tree[id * 2] + self.__tree[id * 2 + 1]

    def __query_up(self, id : int, left : int, right : int):
        """ 
        Find the closest floor with a task
        """
        if (left == right):
            if (self.__tree[id] > 0):
                return left 
            return -1

        mid = (left + right) // 2

        # left first
        if (self.__tree[id * 2] > 0):
            return self.__query_up(id * 2, left, mid)

        if (self.__tree[id * 2 + 1] > 0):
            return self.__query_up(id * 2 + 1, mid + 1, right)

        return -1

    def query_up(self, current_floor):
        return self.__query_up(1, current_floor, self.__num_floors)

    def __query_down(self, id, left : int, right : int):
        """ 
        Find the closest floor with a task
        """
        if (left == right):
            if (self.__tree[id] > 0):
                return left 
            return -1

        mid = (left + right) // 2

        # right first
        if (self.__tree[id * 2 + 1] > 0):
            return self.__query_up(id * 2 + 1, mid + 1, right)

        if (self.__tree[id * 2] > 0):
            return self.__query_up(id * 2, left, mid)
        return -1

    def query_down(self, current_floor):
        """ 
        Find the closest floor with a task
        """
        return self.__query_down(1, 1, current_floor)

    def add_task(self, floor: int, task : int):
        """
        Floor i has tasks with 2 type:
        = 0: Drop passenger at floor i
        > 0: Pick up passenger at floor i and move there.
        """

        if (floor < 1 or floor > self.__num_floors):
            # logging.warning("Request invalid floor!" + " " + str(floor) + " " + str(self.__num_floors))
            return False
        if (task < 0 or task > self.__num_floors):
            # logging.warning("Request invalid tasks!" + " " + str(floor) + " " + str(self.__num_floors))
            return False

        # Noone is going to the same floor!!!!
        if (floor == task):
            return False

        self.__tasks_sets[floor].add(task)

        if (get_settings().testing):
            print("Number of tasks", floor, len(self.__tasks_sets[floor]))

        num_tasks = len(self.__tasks_sets[floor])
        self.__mod_tree(1, 1, self.__num_floors, floor, num_tasks)
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
                self.__mod_tree(1, 1, self.__num_floors, next_floor, num_tasks)

        # Should be 0 -> mock test this? 
        num_tasks = len(__tasks_sets[floor])

        self.__mod_tree(1, 1, self.__num_floors, floor, num_tasks)
