from datetime import timedelta

from pytest_mock import MockerFixture
from robot.api import logger

from Mainframe3270.utils import (
    SearchResultMode,
    convert_timeout,
    coordinates_to_dict,
    prepare_position_as,
    prepare_positions_as,
)


def test_convert_timeout_with_timedelta():
    timeout = convert_timeout(timedelta(seconds=30))

    assert timeout == 30.0


def test_convert_timeout_with_timestring():
    timeout = convert_timeout("1 minute")
    assert timeout == 60.0


def test_prepare_position_as():
    assert prepare_position_as((5, 5), SearchResultMode.As_Tuple) == (5, 5)


def test_prepare_position_as_dict():
    assert prepare_position_as((5, 6), SearchResultMode.As_Dict) == {"ypos": 5, "xpos": 6}


def test_prepare_positions_as():
    assert prepare_positions_as([(5, 5)], SearchResultMode.As_Tuple) == [(5, 5)]


def test_prepare_positions_as_dict():
    assert prepare_positions_as([(5, 6)], SearchResultMode.As_Dict) == [{"ypos": 5, "xpos": 6}]


def test_prepare_positions_as_invalid_mode(mocker: MockerFixture):
    mocker.patch("robot.api.logger.warn")

    assert prepare_positions_as([(5, 10)], "abc") == [(5, 10)]

    logger.warn.assert_called_with(
        '"mode" should be either "SearchResultMode.As_Dict" or "SearchResultMode.As_Tuple". '
        "Returning the result as tuple"
    )


def test_coordinates_to_dict():
    assert coordinates_to_dict(1, 5) == {"ypos": 1, "xpos": 5}
