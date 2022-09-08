"""An object to manage a task."""


from dirty import set_state
from utilities import human_duration


class Task:
    """Wrapper around a boinc task"""

    def __init__(self, json_task):
        """Initialize from a json."""
        self.json_task = json_task
        self.remaining = json_task["remaining"]
        self.human_remaining = human_duration(self.remaining)
        self.name = json_task["name"]
        self.active_state = json_task["active_task_state"]
        self.project_url = json_task["project_url"]
        self.ready_to_report = json_task["ready_to_report"]

    def is_started(self):
        """Say if the computation is already started."""
        elapsed = float(self.json_task["elapsed task time"])
        return elapsed > 0

    def resume(self):
        """Resume the task."""
        set_state(self, "resume")

    def suspend(self):
        """Suspend the task."""
        set_state(self, "suspend")
