from datetime import timedelta

from Mainframe3270.utils import convert_timeout


def test_convert_timeout_with_timedelta():
    timeout = convert_timeout(timedelta(seconds=30))

    assert timeout == 30.0


def test_convert_timeout_with_timestring():
    timeout = convert_timeout("1 minute")
    assert timeout == 60.0
