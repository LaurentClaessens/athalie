#!venv/bin/python3


from station import Station
from utilities import human_timestamp


def make_me_happy():
    """Do the work."""
    from pathlib import Path
    logfile = Path('./ath.log')
    logfile.write_text(human_timestamp())
    with Station() as station:
        station.resume_all()
        tasks = station.by_remaining()

        ok_tasks = [tasks[0], tasks[-1], tasks[-2]]
        for task in station:
            if task not in ok_tasks:
                task.suspend()


make_me_happy()
