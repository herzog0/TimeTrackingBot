from typing import Union


def seconds_to_str(seconds: Union[int, float]):
    seconds = int(seconds)
    d = seconds//3600, (seconds//60) % 60
    return f"{d[0]}h{d[1]}m"
