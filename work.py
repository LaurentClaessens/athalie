#!venv/bin/python3


import time
from src.utilities import human_timestamp
from src.utilities import human_seconds
from src.utilities_b import get_project_prio
from src.utilities_b import list_duration
from src.station import Station

dprint = print


def do_work(station):
    """Do the work."""
    now = time.time()
    tot_dur = list_duration(station)
    tot_finish = now + tot_dur
    print(f"{human_seconds(tot_dur)} -> {human_timestamp(tot_finish)}")

    prio = get_project_prio(station)

    print("---- ma sélection ----")
    for task in prio:
        print(task.project_name, task.human_remaining)


with Station() as station:
    do_work(station)
