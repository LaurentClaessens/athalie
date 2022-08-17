"""Here are the functions making the dirty work."""


import sys
import subprocess
_ = sys


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

        if key == "project URL":
            reparts = line.split(" URL:")
            url = reparts[1].strip()
            task["project_url"] = url
        if key == "estimated CPU time remaining":
            task["remaining"] = float(value)
    return task


def get_json_tasks():
    """Return the list of tasks as json like object."""
    b_output = subprocess.check_output(['boinccmd', '--get_tasks'], timeout=2)
    text = b_output.decode('utf8')
    paks = text.split(") -----------")
    tasks = []
    for pak in paks:
        task = pak_to_task(pak)
        if task:
            # The first element in the text split is
            # ======== Tasks ========
            # 1
            # which do not correspond to a task.
            tasks.append(task)
    return tasks


def set_state(task, state):
    """Suspend a task"""
    project_url = task.project_url
    name = task.name
    subprocess.run(['boinccmd', '--task', project_url, name, state])
