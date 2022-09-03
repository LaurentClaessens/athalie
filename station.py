"""Your work station. This is a set of tasks."""

import time
from task import Task
from dirty import get_json_tasks


dprint = print


class Station:
    """
    Wrapper around a list of tasks.

    You can use this class as a context manager to resume
    all the tasks when exiting.
    """

    def __init__(self):
        """Initialize"""
        json_tasks = get_json_tasks()
        self.tasks = [Task(task) for task in json_tasks
                      if not task["ready_to_report"]]

    def by_remaining(self):
        """Return the list of tasks sorted by remaining time."""
        self.tasks.sort(key=lambda task: task.remaining)
        return self.tasks

    def remaining(self):
        """The total remaining time."""
        return sum(task.remaining for task in self)

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
