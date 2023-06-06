from datetime import timedelta

from robot.utils import timestr_to_secs


def convert_timeout(time):
    if isinstance(time, timedelta):
        return time.total_seconds()
    return timestr_to_secs(time, round_to=None)
