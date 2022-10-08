"""Your work station. This is a set of tasks."""

import time
from task import Task
from project import Project
from dirty import get_json_tasks
from dirty import get_boinccmd_json
_ = [get_json_tasks]


dprint = print


class Station:
    """
    Wrapper around a list of tasks.

    You can use this class as a context manager to resume
    all the tasks when exiting.
    """

    def __init__(self):
        """Initialize"""
        # json_tasks = get_json_tasks()
        json_tasks = get_boinccmd_json("--get_tasks")
        self.tasks = [Task(task) for task in json_tasks
                      if not task["ready_to_report"]]
        project_jsons = get_boinccmd_json("--get_project_status")
        self.projects = [Project(proj_json, self)
                         for proj_json in project_jsons]

        for project in self.projects:
            for task in project:
                task.project = project

    def by_remaining(self):
        """Return the list of tasks sorted by remaining time."""
        self.tasks.sort(key=lambda task: task.remaining)
        return self.tasks

    def remaining(self):
        """The total remaining time."""
        return sum(task.remaining for task in self)

    def get_project_task(self, project_name):
        """Return the list of tasks of the requested project."""
        return [task for task in self if task.project_name == project_name]

    def resume_all(self):
        """Resume all tasks."""
        time.sleep(1)
        [task.resume() for task in self]

    def __enter__(self):
        """Initiate self as a context manager"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Resume all the tasks."""
        self.resume_all()

    def __getitem__(self, index):
        """Make Station iterable over the tasks."""
        return self.tasks[index]

    def __len__(self):
        return len(self.tasks)
