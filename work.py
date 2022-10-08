#!venv/bin/python3


import time


from src.utilities import ColorPrint
from src.utilities import human_seconds
from src.utilities import human_duration
from src.utilities import human_timestamp
from src.utilities_b import list_duration
from src.station import Station

dprint = print


def do_work(station):
    """Do the work."""
    now = time.time()
    tot_dur = list_duration(station)
    tot_finish = now + tot_dur
    print(f"{human_seconds(tot_dur)} -> {human_timestamp(tot_finish)}")

    for task in station.by_remaining():
        color = task.project.color
        my_str = human_duration(task.my_remaining())
        pr_str = task.human_remaining.ljust(9)
        with ColorPrint(color):
            print(task.project_name.ljust(8), pr_str, my_str)


with Station() as station:
    do_work(station)
