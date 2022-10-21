"""Utilities for athalie."""


import time
import contextlib

from src.utilities import human_duration
from src.utilities import read_json_file
from src.utilities import human_timestamp


dprint = print


def get_standard(obj, new_tasks=True, indexes=None):
    """First and two lasts."""
    if indexes is None:
        indexes = [-1, -2, 0]
    tasks = obj.by_remaining()
    if not new_tasks:
        tasks = [task for task in tasks if task.is_started()]

    answer = []
    with contextlib.suppress(IndexError):
        for idx in indexes:
            answer.append(tasks[idx])

    return answer


def get_project_prio(station):
    """Return the tasks of the projects sorted by project priority."""
    prio = []
    for name in ["lhc", "rosetta", "mlc", "wcg"]:
        project = station.get_project(name)
        pr_prio = get_standard(project, indexes=[0, -1, -2])
        prio.extend(pr_prio)

    projects = station.projects
    projects.sort(key=lambda x: x.credit)
    for project in station.projects:
        pr_prio = get_standard(project, indexes=[0, -1, -2])
        prio.extend(pr_prio)
    return prio


def is_hurry(task, hurry_strs):
    """Say if a task is in a hurry."""
    str_deadline = task.json_task["report deadline"]
    # print(str_deadline)
    for hurry_str in hurry_strs:
        if hurry_str in str_deadline:
            return True
    return False


def remove_duplicates(my_list):
    """Remove duplicates of the list."""
    answer = []
    for task in my_list:
        if task not in answer:
            answer.append(task)
    return answer


def get_hurry(station, new_tasks=True):
    """Add the task in a hurry."""
    hurry_strs = read_json_file("hurry_strings.json")
    prio = []
    tasks = station.by_remaining()
    tasks.reverse()
    if not new_tasks:
        tasks = [task for task in tasks if task.is_started()]

    prio = [task for task in tasks if is_hurry(task, hurry_strs)]
    hurry_duration = list_duration(prio)
    end_time = time.time() + hurry_duration

    print(
        f"hurry {human_duration(hurry_duration)} -> "
        f"{human_timestamp(end_time)}")

    prio = remove_duplicates(prio)
    return prio


def list_duration(task_list, my_duration=False):
    """Say the duration of a task list"""
    length = sum(task.remaining for task in task_list)
    if my_duration:
        length = sum(task.my_remaining() for task in task_list)
    return length / 3
