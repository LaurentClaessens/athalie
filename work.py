#!venv/bin/python3


import time
from utilities import human_timestamp
from utilities import human_seconds
from station import Station


def do_work(station):
    """Do the work."""
    tasks = [task for task in station.by_remaining()
             if task.is_started()]
    total = sum(task.remaining for task in tasks) / 3
    now = time.time()
    end_time = now + total
    print(f"{human_seconds(total)} -> {human_timestamp(end_time)}")


with Station() as station:
    do_work(station)
