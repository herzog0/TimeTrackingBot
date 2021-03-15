from datetime import timedelta
from typing import Union


def seconds_to_str(seconds: Union[int, float]):
    seconds = int(seconds)
    d = str(timedelta(seconds=seconds))
    d = d.split(':')
    return f"{d[0]}h{d[1]}m"
