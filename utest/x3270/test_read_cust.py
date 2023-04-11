import pytest
from pytest_mock import MockerFixture

from Mainframe3270.x3270 import X3270


def test_read_fails_check_y_axis_limit_cust(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
            Exception, match="You have exceeded the y-axis limit of the mainframe screen"
    ):
        under_test.read(44, 1, 1)


def test_read_fails_check_x_axis_limit_cust(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    with pytest.raises(
            Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        under_test.read(1, 133, 1)


def test_read_exceeds_x_axis_cust(under_test: X3270, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")

    with pytest.raises(
            Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        under_test.read(1, 132, 5)
