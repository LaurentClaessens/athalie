#!venv/bin/python3


from station import Station
from utilities import human_timestamp


dprint = print


def may_append(my_list, obj):
    """Append if not present."""
    if obj not in my_list:
        my_list.append(obj)


def get_hurry(station):
    """Add the task in a hurry."""
    prio = []
    tasks = station.by_remaining()
    tasks.reverse()
    for task in station:
        str_deadline = task.json_task["report deadline"]
        print(str_deadline)
        if "Tue Sep 4" in str_deadline:
            prio.append(task)
    return prio


def get_standard(station):
    """First and two lasts."""
    tasks = station.by_remaining()
    return([tasks[0], tasks[-1], tasks[-2]])


def get_last(station):
    """Three last tasks."""
    tasks = station.by_remaining()
    return([tasks[-1], tasks[-2], tasks[-3]])


def get_gap_index(station):
    """Return the index of the task with gap."""
    tasks = station.by_remaining()
    previous = tasks[0]
    for num, task in enumerate(tasks[1:]):
        if task.remaining - previous.remaining > 1.5*3600:
            return num + 1
    return None


def get_gapped(station):
    """If there is a 1 hour gap between two tasks, return the three lasts."""
    gap_index = get_gap_index(station)
    if gap_index is None:
        return []

    tasks = station.by_remaining()
    dprint("je vois un gap à la position", gap_index)
    ok_tasks = tasks[gap_index:]
    print(len(ok_tasks))

    return get_last(station)


def prioritary_tasks(station):
    """Return a list of task to be prioritized."""
    prio = []
    prio.extend(get_hurry(station))
    prio.extend(get_gapped(station))
    prio.extend(get_standard(station))

    filtered = []
    for task in prio:
        if task not in filtered:
            filtered.append(task)

    return filtered


def make_me_happy():
    """Do the work."""
    from pathlib import Path
    logfile = Path('./ath.log')
    logfile.write_text(human_timestamp())
    with Station() as station:
        station.resume_all()
        prio = prioritary_tasks(station)
        ok_tasks = prio[0:3]

        for task in station:
            if task not in ok_tasks:
                task.suspend()


make_me_happy()
