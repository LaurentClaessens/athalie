"""Here are the functions making the dirty work."""


import subprocess


dprint = print


def pak_to_task(pak):
    """Return a json like task from its output"""
    task = {}
    for line in pak.splitlines():
        if ": " not in line:
            continue
        parts = line.split(":")
        key = parts[0].strip()
        value = parts[1].strip()
        task[key] = value
    return task


def get_json_tasks():
    """Return the list of tasks as json like object."""
    b_output = subprocess.check_output(['boinccmd', '--get_tasks'], timeout=2)
    text = b_output.decode('utf8')
    paks = text.split(") -----------")
    tasks = []
    for pak in paks:
        task = pak_to_task(pak)
        tasks.append(task)
