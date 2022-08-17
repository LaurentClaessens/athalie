#!venv/bin/python3


from dirty import get_json_tasks
from task import Task


def do_work():
    """Do the work."""
    json_tasks = get_json_tasks()
    tasks = [Task(task) for task in json_tasks]
    tasks.sort(key=lambda task: task.remaining)

    for task in tasks:
        print(task.remaining)


do_work()
