"""An object to manage a task."""


from src.dirty import url_to_name
from src.dirty import set_state
from src.utilities import human_duration

dprint = print


class Task:
    """Wrapper around a boinc task"""

    def __init__(self, json_task):
        """Initialize from a json."""
        self.json_task = json_task
        self.remaining = json_task["remaining"]
        self.human_remaining = human_duration(self.remaining)
        self.name = json_task["name"]
        self.active_state = json_task["active_task_state"]
        self.ready_to_report = json_task["ready_to_report"]
        self.project_url = self.json_task["project_url"]
        self.project_name = url_to_name[self.project_url]
        self.elapsed = float(self.json_task["elapsed task time"])
        self.fraction_done = float(self.json_task.get("fraction done", 0))
        self.project = None

    def is_started(self):
        """Say if the computation is already started."""
        elapsed = float(self.json_task["elapsed task time"])
        return elapsed > 0

    def my_remaining(self):
        """Say my estimation of remaining."""
        if self.fraction_done == 0:
            return self.remaining
        total_time = self.elapsed / self.fraction_done
        remaining = total_time - self.elapsed
        return remaining

    def resume(self):
        """Resume the task."""
        set_state(self, "resume")

    def suspend(self):
        """Suspend the task."""
        set_state(self, "suspend")
