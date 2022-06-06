import sys
sys.path.append('../src')

from task_tree import TaskTree
import pytest

def test_task_tree_init():
    tasktree = TaskTree(num_floors = 100)

    # from floor 1 to floor 10
    ans = tasktree.add_task(1, 10)
    assert(ans)
    assert(2 == len(tasktree._TaskTree__tasks_sets[1]))

    # request from floor 2 to 30
    ans = tasktree.add_task(1, 30)
    assert(ans)
    assert(3 == len(tasktree._TaskTree__tasks_sets[1]))

    ans = tasktree.add_task(1, 40)

    assert(ans)
    assert(2 == len(tasktree._TaskTree__tasks_sets[1]))

    ans = tasktree.add_task(30, 0)

    assert(ans)
    assert(1 == len(tasktree._TaskTree__tasks_sets[30]))

    tasktree.fullfill_all_tasks_on_floor(1)

    assert(len(tasktree._TaskTree__tasks_sets[30]) == 2)
    assert(tasktree._TaskTree__num_floors == 100)
    assert(tasktree._TaskTree__tree[1] == 3)


def test_task_tree_tasks_query_up():
    tasktree = TaskTree(num_floors = 100)
    # from floor 1 to floor 10
    ans = tasktree.add_task(4, 0)
    assert(ans)
    # request from floor 2 to 30
    ans = tasktree.add_task(5, 0)
    assert(ans)

    ans = tasktree.add_task(10, 0)
    assert(ans)
    ans = tasktree.add_task(11, 0)
    assert(ans)
    ans = tasktree.add_task(12, 0)
    assert(ans)
    ans = tasktree.add_task(13, 0)
    assert(ans)
    ans = tasktree.add_task(14, 0)
    assert(ans)

    ans = tasktree.add_task(15, 0)
    ans = tasktree.query_up(10)

    assert(ans == 10)
