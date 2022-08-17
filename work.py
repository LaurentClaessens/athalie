#!venv/bin/python3


import time
from station import Station


def do_work():
    """Do the work."""
    with Station() as station:
        tasks = station.by_remaining()

        ok_tasks = [tasks[0], tasks[-1], tasks[-2]]
        for task in station:
            print(task.remaining)
            if task not in ok_tasks:
                task.suspend()

        time.sleep(1)
        station.resume_all()


do_work()
