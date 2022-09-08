#!venv/bin/python3


import time
from utilities import get_hurry
from utilities import human_timestamp
from utilities import human_seconds
from utilities import list_duration
from station import Station

dprint = print


def do_work(station):
    """Do the work."""
    now = time.time()
    tot_dur = list_duration(station)
    tot_finish = now + tot_dur
    print(f"{human_seconds(tot_dur)} -> {human_timestamp(tot_finish)}")


with Station() as station:
    do_work(station)
