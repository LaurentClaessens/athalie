#!venv/bin/python3


from station import Station
from utilities import human_timestamp
from utilities import human_duration
from utilities import get_hurry


dprint = print


def may_append(my_list, obj):
    """Append if not present."""
    if obj not in my_list:
        my_list.append(obj)


def get_standard(station, new_tasks=True):
    """First and two lasts."""
    tasks = station.by_remaining()
    if not new_tasks:
        tasks = [task for task in tasks if task.is_started()]
    return([tasks[-1], tasks[-2], tasks[0]])


def get_last(station):
    """Three last tasks."""
    tasks = station.by_remaining()
    return([tasks[-1], tasks[-2], tasks[-3]])


def get_gap_index(station):
    """Return the index of the task with gap."""
    tasks = station.by_remaining()
    previous = tasks[0]
    for num, task in enumerate(tasks[0:]):
        delta = task.remaining - previous.remaining
        if delta > 30 * 60:
            if num != 1:
                # A gap on first position is ok.
                print(f"gap {human_duration(delta)} at position {num+1}: "
                      f"{human_duration(previous.remaining)} --> "
                      f" -> {human_duration(task.remaining)}")
                return num
        previous = task
    return None


def get_gapped(station):
    """If there is a 1 hour gap between two tasks, return the three lasts."""
    gap_index = get_gap_index(station)
    if gap_index is None:
        return []

    tasks = station.by_remaining()
    ok_tasks = tasks[gap_index:]
    ok_tasks.reverse()

    return ok_tasks


def prioritary_tasks(station):
    """Return a list of task to be prioritized."""
    prio = []
    hurry_strs = ["Mon Sep 19"]
    prio.extend(get_hurry(station, hurry_strs))

    prio.extend(get_gapped(station))
    prio.extend(get_standard(station))

    filtered = []
    for task in prio:
        if task not in filtered:
            filtered.append(task)
    return filtered


def make_me_happy(station):
    """Do the work."""
    from pathlib import Path
    logfile = Path('./ath.log')
    logfile.write_text(human_timestamp())
    station.resume_all()
    prio = prioritary_tasks(station)
    ok_tasks = prio[0:3]

    print("selectionnées:")
    for task in ok_tasks:
        print(task.human_remaining)

    for task in station:
        if task not in ok_tasks:
            task.suspend()


with Station() as station:
    make_me_happy(station)
