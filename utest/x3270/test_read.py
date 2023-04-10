import pytest
from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import X3270


def test_read(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    string = under_test.read(1, 1, 3)

    Emulator.string_get.assert_called_once_with(1, 1, 3)
    assert string == "abc"


def test_read_fails_check_y_axis_limit(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
        Exception, match="You have exceeded the y-axis limit of the mainframe screen"
    ):
        under_test.read(25, 1, 1)


def test_read_fails_check_x_axis_limit(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
        Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        under_test.read(1, 81, 1)


def test_read_exceeds_x_axis(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
        Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        under_test.read(1, 80, 2)


def test_read_all_screen(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")
    content = under_test.read_all_screen()
    assert content == "a" * 24
