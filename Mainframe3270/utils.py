from datetime import timedelta

from robot.utils import timestr_to_secs


def convert_timeout(time):
    if isinstance(time, timedelta):
        return time.total_seconds()
    return timestr_to_secs(time, round_to=None)


def coordinate_tuple_to_dict(coordinate_tuple):
    if not isinstance(coordinate_tuple, tuple):
        raise TypeError(f"Input must be instance of {tuple}")
    if len(coordinate_tuple) != 2:
        raise ValueError(f"Length of input must be 2, but was {len(coordinate_tuple)}")
    return {"ypos": coordinate_tuple[0], "xpos": coordinate_tuple[1]}
