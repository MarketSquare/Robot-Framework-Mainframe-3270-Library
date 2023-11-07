from datetime import timedelta
from enum import Enum, auto

from robot.utils import timestr_to_secs


class SearchResultMode(Enum):
    As_Tuple = auto()
    As_Dict = auto()


def convert_timeout(time):
    if isinstance(time, timedelta):
        return time.total_seconds()
    return timestr_to_secs(time, round_to=None)


def coordinates_to_dict(ypos: int, xpos: int):
    return {"ypos": ypos, "xpos": xpos}
