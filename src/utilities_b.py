"""Utilities for athalie."""


import sys
import datetime
import contextlib

from src.utilities import ciao
from src.utilities import read_json_file
_ = sys, ciao


dprint = print


def str_to_day(str_date: str):
    """
    Return the datetime of the days given by the string.

    This function accepts inputs like this:
    Tue Apr 11 02:05:15 2023
    """
    str_format = "%a %b %d %H:%M:%S %Y"
    date = datetime.datetime.strptime(str_date, str_format).date()
    year = date.year
    month = date.month
    day = date.day
    return datetime.datetime(year, month, day)


def is_date_hurry(str_date: str) -> bool:
    """Say if the given date is too short."""
    today = datetime.datetime.now()

    due_day = str_to_day(str_date)

    delta = datetime.timedelta(days=3)
    end_hurry = today + delta
    return due_day < end_hurry


def get_standard(obj, new_tasks=True, indexes=None):
    """First and two lasts."""
    if indexes is None:
        indexes = [-1, -2, 0]
    try:
        tasks = obj.by_remaining()
    except AttributeError:
        # Assume 'obj' is a list of tasks
        obj.sort(key=lambda x: x.remaining)
        tasks = obj

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
    projects = station.projects
    projects.sort(key=lambda x: x.credit)
    for project in station.projects:
        indexes = [0, -1, -2]
        if project.project_name == "einstein":
            indexes = [0, 1, 2]
        pr_prio = get_standard(project, indexes=indexes)
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
    hurry_parms = read_json_file("hurry_strings.json")
    hurry_strs = hurry_parms["dates"]
    hurry_names = hurry_parms["task_names"]
    prio = []
    tasks = station.by_remaining()
    tasks.reverse()
    if not new_tasks:
        tasks = [task for task in tasks if task.is_started()]

    h_tasks = [task for task in tasks if is_hurry(task, hurry_strs)]
    prio = get_standard(h_tasks, indexes=[-1, -2, 0])
    prio.extend(h_tasks)

    for task in tasks:
        for name in hurry_names:
            if name in task.name:
                prio.insert(0, task)

    date_hurry_tasks = station.date_hurry_tasks()
    date_prio = get_standard(date_hurry_tasks, indexes=[-1,-2, -3])

    prio = date_prio + prio

    prio = remove_duplicates(prio)
    return prio


def list_duration(task_list, my_duration=False):
    """Say the duration of a task list"""
    length = sum(task.remaining for task in task_list)
    if my_duration:
        length = sum(task.my_remaining() for task in task_list)
    return length / 3
