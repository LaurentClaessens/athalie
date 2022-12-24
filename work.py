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
    now = time.time()
    for task in tasks:
        color = task.project.color
        pr_str = task.human_remaining.ljust(9)
        my_str = human_duration(task.my_remaining()).ljust(9)
        deadline = task.report_deadline_str
        deadline = ""

        format_str = "%H:%M"
        end_time = now + task.remaining
        boinc_previsions = human_timestamp(end_time, format_str=format_str)
        end_time = now + task.my_remaining()
        my_previsions = human_timestamp(end_time, format_str=format_str)

        previsions = f"lui: {boinc_previsions}, moi: {my_previsions}"

        active = ["", previsions][task.active_state == "EXECUTING"]
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
    print_summary(station.by_remaining())
    h_tasks = get_hurry(station)
    if not h_tasks:
        print("No prioritary tasks. Here is the total.")
        h_tasks = station

    print_previsions(h_tasks)


station = Station()
do_work(station)
