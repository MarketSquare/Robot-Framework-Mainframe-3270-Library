from datetime import timedelta

from Mainframe3270.utils import convert_timeout, coordinates_to_dict


def test_convert_timeout_with_timedelta():
    timeout = convert_timeout(timedelta(seconds=30))

    assert timeout == 30.0


def test_convert_timeout_with_timestring():
    timeout = convert_timeout("1 minute")
    assert timeout == 60.0


def test_coordinates_to_dict():
    assert coordinates_to_dict(1, 5) == {"ypos": 1, "xpos": 5}
