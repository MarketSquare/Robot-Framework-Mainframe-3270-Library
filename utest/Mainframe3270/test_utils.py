from datetime import timedelta

import pytest

from Mainframe3270.utils import convert_timeout, coordinate_tuple_to_dict


def test_convert_timeout_with_timedelta():
    timeout = convert_timeout(timedelta(seconds=30))

    assert timeout == 30.0


def test_convert_timeout_with_timestring():
    timeout = convert_timeout("1 minute")
    assert timeout == 60.0


def test_coordinate_tuple_to_dict():
    assert coordinate_tuple_to_dict((1, 5)) == {"ypos": 1, "xpos": 5}


def test_coordinate_tuple_to_dict_with_wrong_input():
    with pytest.raises(TypeError, match="Input must be instance of <class 'tuple'>"):
        coordinate_tuple_to_dict(1)


def test_coordinate_tuple_to_dict_with_invalid_length():
    with pytest.raises(ValueError, match="Length of input must be 2, but was 3"):
        coordinate_tuple_to_dict((2, 4, 6))
