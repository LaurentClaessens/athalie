#!venv/bin/python3


import time


from src.utilities import ColorPrint
from src.utilities import human_seconds
from src.utilities import human_duration
from src.utilities import human_timestamp
from src.utilities_b import list_duration
from src.utilities_b import get_hurry
from src.station import Station

dprint = print


def print_summary(tasks):
    """Print a summary of the tasks."""
    for task in tasks:
        color = task.project.color
        my_str = human_duration(task.my_remaining()).ljust(8)
        pr_str = task.human_remaining.ljust(8)
        active = ["", "*"][task.active_state == "EXECUTING"]
        with ColorPrint(color):
            print(task.project_name.ljust(8), pr_str, my_str, active)

    now = time.time()
    tot_dur = list_duration(tasks)
    tot_finish = now + tot_dur
    print(f"{human_seconds(tot_dur)} -> {human_timestamp(tot_finish)}")


def do_work(station):
    """Do the work."""
    h_tasks = get_hurry(station)

    print_summary(station.by_remaining())
    print("--")
    print_summary(h_tasks)


with Station() as station:
    do_work(station)
