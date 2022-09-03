"""Some utilities"""

import time
import math
import json
import string
import random
import datetime
import contextlib
from pathlib import Path


def human_duration(duration):
    """Write a human readable duration (in seconds)"""
    # days = int(duration // 86400)
    hours = int(duration // 3600 % 24)
    minutes = int(duration // 60 % 60)
    seconds = int(duration % 60)
    return f"{hours}h{minutes}m{seconds}s"


def random_string(length):
    """Return a random string of letters of the given length."""
    rn_list = [random.choice(string.ascii_letters) for i in range(1, length)]
    return "".join(rn_list)


def human_timestamp(now=None):
    """Return a human readable timestamp."""
    if now is None:
        now = time.time()
    local_time = time.localtime(now)
    return time.strftime("%Z - %A  %Y/%B/%d, %H:%M:%S", local_time)


def json_serial(obj):
    """Serialize the datetime."""
    if isinstance(obj, datetime.datetime):
        timestamp = obj.timestamp()
        return human_timestamp(timestamp)
    with contextlib.suppress(AttributeError):
        return obj.to_json()
    return str(obj)


def json_to_str(json_dict, pretty=False, default=None):
    """Return a string representation of the given json."""
    if pretty:
        return json.dumps(json_dict,
                          sort_keys=True,
                          indent=4,
                          default=json_serial)
    return json.dumps(json_dict, default=json_serial)


def write_json_file(json_dict,
                    filename,
                    pretty=False,
                    default=None,
                    parents=False):
    """Write the dictionary in the given file."""
    if parents:
        parent = filename.parent
        parent.mkdir(parents=True, exist_ok=True)
    my_str = json_to_str(json_dict, pretty=pretty, default=default)
    with open(filename, 'w') as json_file:
        json_file.write(my_str)


def read_json_file(json_path, default=None):
    """
    Return the given json file as dictionary.

    @param {string} `json_path`
    @return {dictionary}
    """
    json_path = Path(json_path)
    if not json_path.is_file():
        if default is None:
            raise ValueError(f"You try to read {json_path}. "
                             f"The file does not exist and you "
                             f"furnished no default.")
        return default
    with open(json_path, 'r') as json_data:
        try:
            answer = json.load(json_data)
        except json.decoder.JSONDecodeError as err:
            print("JSONDecodeError:", err)
            message = f"Json error in {json_path}:\n {err}"
            raise ValueError(message) from err
    return answer


def human_seconds(total):
    """
    Return a human readable time.

    `total` is a number of seconds and we return xxh:yym:zzs
    """
    hours = math.floor(total / 3600)
    remainder = total - 3600 * hours
    minutes = math.floor(remainder / 60)
    remainder = remainder - 60 * minutes
    seconds = round(remainder)
    return f"{hours}h:{minutes}m:{seconds}s"
