#!venv/bin/python3


import time
from station import Station
from utilities import human_duration
from utilities import human_timestamp


def do_work():
    """Do the work."""
    with Station() as station:
        total = station.remaining()
        average = total / len(station)
        duration = total / 3
        now = time.time()
        end_time = now + duration
        print(human_duration(duration), '-->', human_timestamp(end_time))

        average_dur = average / 3
        print(human_duration(average_dur))


do_work()
