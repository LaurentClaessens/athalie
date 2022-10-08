"""A class representing a project."""


from src.dirty import url_to_name

dprint = print


class Project:
    """A boinc project."""

    def __init__(self, project_json, station):
        """Initialize"""
        self.station = station
        self.project_json = project_json
        self.credit = self.project_json["user_total_credit"]
        self.project_url = self.project_json["master URL"]
        self.project_name = url_to_name[self.project_url]
        self.tasks = [task for task in self.station
                      if task.project_name == self.project_name]
        self.color = self.get_color()

    def get_color(self):
        """Say the project's color."""
        if self.project_name == "rosetta":
            return "green"
        if self.project_name == "sidock":
            return "red"
        if self.project_name == "einstein":
            return "yellow"
        return "black"

    def show_json(self):
        print("=====================================")
        for key, value in self.project_json.items():
            print(f"{key} --> {value}")
        print("=====================================")

    def by_remaining(self):
        """Return the list of tasks sorted by remaining time."""
        self.tasks.sort(key=lambda task: task.remaining)
        return self.tasks

    def __getitem__(self, index):
        """Make Station iterable over the tasks."""
        return self.tasks[index]

    def __len__(self):
        return len(self.tasks)
