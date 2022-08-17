"""An object to manage a task."""


class Task:
    """Wrapper around a boinc task"""

    def __init__(self, json_task):
        """Initialize from a json."""
        self.json_task = json_task
        self.remaining = json_task["remaining"]
