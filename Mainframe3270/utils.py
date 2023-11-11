from datetime import timedelta
from enum import Enum, auto
from typing import List, Tuple

from robot.api import logger
from robot.utils import timestr_to_secs


class SearchResultMode(Enum):
    As_Tuple = auto()
    As_Dict = auto()


def prepare_position_as(position: Tuple[int, int], mode: SearchResultMode):
    return prepare_positions_as([position], mode)[0]


def prepare_positions_as(positions: List[Tuple[int, int]], mode: SearchResultMode):
    if mode == SearchResultMode.As_Dict:
        return [coordinates_to_dict(ypos, xpos) for ypos, xpos in positions]
    elif mode == SearchResultMode.As_Tuple:
        return positions
    else:
        logger.warn(
            f'"mode" should be either "{SearchResultMode.As_Dict}" or "{SearchResultMode.As_Tuple}". '
            "Returning the result as tuple"
        )
        return positions


def convert_timeout(time):
    if isinstance(time, timedelta):
        return time.total_seconds()
    return timestr_to_secs(time, round_to=None)


def coordinates_to_dict(ypos: int, xpos: int):
    return {"ypos": ypos, "xpos": xpos}
