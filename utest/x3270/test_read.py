import pytest
from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator


def test_read(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    string = Emulator().read(1, 1, 3)

    Emulator.string_get.assert_called_once_with(1, 1, 3)
    assert string == "abc"


def test_read_fails_check_y_axis_limit(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
        Exception, match="You have exceeded the y-axis limit of the mainframe screen"
    ):
        Emulator().read(44, 1, 1)


def test_read_fails_check_x_axis_limit(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
        Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        Emulator().read(1, 133, 1)


def test_read_exceeds_x_axis(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
        Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        Emulator().read(1, 80, 2)


def test_read_all_screen(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")
    content = Emulator().read_all_screen()
    assert content == "a" * 24
