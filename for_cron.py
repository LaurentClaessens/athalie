#!venv/bin/python3

import sys

from src.station import Station
from src.utilities_b import get_hurry
from src.utilities_b import get_standard
from src.utilities_b import get_project_prio
from src.utilities import human_duration
from src.utilities import human_timestamp
_ = [sys]


dprint = print


def may_append(my_list, obj):
    """Append if not present."""
    if obj not in my_list:
        my_list.append(obj)


def get_last(station):
    """Three last tasks."""
    tasks = station.by_remaining()
    return([tasks[-1], tasks[-2], tasks[-3]])


def get_gap_index(station):
    """Return the index of the task with gap."""
    tasks = station.by_remaining()
    previous = tasks[0]
    indices = []
    for num, task in enumerate(tasks[0:]):
        delta = task.remaining - previous.remaining
        if delta > 60 * 60:
            if num != 1:
                # A gap on first position is ok.
                print(f"gap {human_duration(delta)} at position {num+1}: "
                      f"{human_duration(previous.remaining)} --> "
                      f"{human_duration(task.remaining)}")
                indices.append({"index": num, "delta": delta})
        previous = task

    if not indices:
        return None
    indices.sort(key=lambda x: x["delta"])
    sel_gap = indices[-1]
    print(f"selected gap: {sel_gap['index'] + 1}"
          f"-- {human_duration(sel_gap['delta'])}")
    return sel_gap["index"]


def get_gapped(station):
    """If there is a 1 hour gap between two tasks, return the three lasts."""
    gap_index = get_gap_index(station)
    if gap_index is None:
        return []

    tasks = station.by_remaining()
    ok_tasks = tasks[gap_index:]
    print("gap task:")
    for task in ok_tasks:
        print("   ", task.human_remaining)
    ok_tasks.reverse()

    return ok_tasks


def make_me_happy(station):
    """Do the work."""
    print("----------")
    print(human_timestamp())
    print("----------")
    station.resume_all()

    hurry_tasks = get_hurry(station)
    project_prio = get_project_prio(station)
    standard = get_standard(station, indexes=[-1, -2, -3])

    sorted_tasks = hurry_tasks + project_prio + standard

    filtered = []
    for task in sorted_tasks:
        if task not in filtered:
            filtered.append(task)

    ok_tasks = filtered[0:3]

    print("selectionnées:")
    for task in ok_tasks:
        print(task.project.project_name, task.human_remaining)

    sys.exit(1)

    for task in station:
        if task not in ok_tasks:
            task.suspend()


with Station() as station:
    make_me_happy(station)
