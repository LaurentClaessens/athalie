"""An object to manage a task."""

import datetime


from src.dirty import url_to_name
from src.dirty import set_state
from src.utilities import human_duration
from src.utilities import human_seconds
from src.utilities import print_json
from src.utilities_b import is_date_hurry
_ = print_json

dprint = print


class Task:
    """Wrapper around a boinc task"""

    def __init__(self, json_task):
        """Initialize from a json."""
        self.json_task = json_task
        self.remaining = json_task.get("remaining", 0)
        self.human_remaining = human_duration(self.remaining)
        self.human_seconds = human_seconds(self.remaining)
        self.name = json_task["name"]
        self.active_state = json_task["active_task_state"]
        self.ready_to_report = json_task["ready_to_report"]
        self.project_url = self.json_task["project_url"]
        self.project_name = url_to_name[self.project_url]

        self.elapsed = float(self.json_task.get("elapsed task time", 0))
        self.fraction_done = float(self.json_task.get("fraction done", 0))
        # self.report_deadline_str = self.json_task['report deadline']

        self.project = None

    def deadline(self)->datetime.datetime:
        """Return the timestamp of the deadline."""
        str_format = "%a %b %d %H:%M:%S %Y"
        str_date = self.json_task['report deadline']
        date = datetime.datetime.strptime(str_date, str_format)
        return date

    def is_date_hurry(self):
        """Say if the task is in a hurry because of a close due date."""
        str_deadline = self.json_task["report deadline"]
        return is_date_hurry(str_deadline)

    def available_to_work(self):
        """Say if the task is available to work."""
        if self.ready_to_report:
            return False
        if self.json_task["state"] == "downloading":
            return False
        if "remaining" not in self.json_task:
            return False

        return True

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
