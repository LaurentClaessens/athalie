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
    tasks.sort(key=lambda x: x.remaining)
    for task in tasks:
        color = task.project.color
        pr_str = task.human_remaining.ljust(9)
        my_str = human_duration(task.my_remaining()).ljust(9)
        deadline = task.report_deadline_str
        deadline = ""
        active = ["", "*"][task.active_state == "EXECUTING"]
        with ColorPrint(color):
            print(deadline, task.project_name.ljust(8), pr_str, my_str, active)


def print_previsions(tasks):
    """Print the previsions."""
    now = time.time()
    tot_dur = list_duration(tasks)
    tot_finish = now + tot_dur
    print(f"lui: {human_seconds(tot_dur)} -> {human_timestamp(tot_finish)}")

    now = time.time()
    tot_dur = list_duration(tasks, my_duration=True)
    tot_finish = now + tot_dur
    print(f"moi: {human_seconds(tot_dur)} -> {human_timestamp(tot_finish)}")


def do_work(station):
    """Do the work."""
    h_tasks = get_hurry(station)

    print_summary(station.by_remaining())
    # print_previsions(station.by_remaining())
    # print("--")
    # print_summary(h_tasks)
    print_previsions(h_tasks)


with Station() as station:
    do_work(station)
