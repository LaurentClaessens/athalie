"""Here are the functions making the dirty work."""


import sys
import subprocess
_ = sys


dprint = print

url_to_name = {
    "https://boinc.bakerlab.org/rosetta/": "rosetta",
    "http://einstein.phys.uwm.edu/": "einstein",
    "https://www.sidock.si/sidock/": "sidock",
    "http://www.worldcommunitygrid.org/": "wcg",
    "https://climateprediction.net/": "climat",
    "http://www.cosmologyathome.org/": "cosmology",
    "https://lhcathome.cern.ch/lhcathome/": "lhc",
    "https://www.mlcathome.org/mlcathome/": "mlc",
    "https://universeathome.pl/universe/": "universe",
    "http://www.rnaworld.de/rnaworld/": "rna worls"
}


def pak_to_task(pak):
    """Return a json like task from its output"""
    task = {}
    for line in pak.splitlines():
        if ": " not in line:
            continue
        parts = line.split(": ")
        key = parts[0].strip()
        value = parts[1].strip()
        task[key] = value

        if key == "project URL":
            reparts = line.split(" URL:")
            url = reparts[1].strip()
            task["project_url"] = url
        if key == "estimated CPU time remaining":
            task["remaining"] = float(value)

        if key == "ready to report":
            if "yes" in value:
                task["ready_to_report"] = True
            if "no" in value:
                task["ready_to_report"] = False

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


def get_boinccmd_json(arg):
    """Return the list of tasks as json like object."""
    b_output = subprocess.check_output(['boinccmd', arg], timeout=2)
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
