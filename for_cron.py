#!venv/bin/python3

import sys

from src.station import Station
from src.utilities_b import get_hurry
from src.utilities_b import get_standard
from src.utilities_b import get_project_prio
from src.utilities import human_duration
from src.utilities import read_json_file
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
    dprint(f"selected gap: {sel_gap['index'] + 1}"
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


def prioritary_tasks(station):
    """Return a list of task to be prioritized."""
    prio = []
    prio.extend(get_hurry(station))
    dprint("Hurry", len(prio))
    prio.extend(get_project_prio(station))

    # prio.extend(get_gapped(station))
    prio.extend(get_standard(station))

    filtered = []
    for task in prio:
        if task not in filtered:
            filtered.append(task)
    return filtered


def make_me_happy(station):
    """Do the work."""
    print("----------")
    print(human_timestamp())
    print("----------")
    station.resume_all()
    prio = prioritary_tasks(station)
    ok_tasks = prio[0:3]

    print("selectionnées:")
    for task in ok_tasks:
        print(task.project.project_name, task.human_remaining)

    for task in station:
        if task not in ok_tasks:
            task.suspend()


with Station() as station:
    make_me_happy(station)
