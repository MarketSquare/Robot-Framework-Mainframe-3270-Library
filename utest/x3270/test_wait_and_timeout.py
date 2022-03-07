import pytest
from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import x3270


def test_change_timeout(under_test: x3270):
    under_test.change_timeout(5)

    assert under_test.timeout == 5


def test_change_wait_time(under_test: x3270):
    under_test.change_wait_time(2.5)

    assert under_test.wait == 2.5


def test_change_wait_time_after_write(under_test: x3270):
    under_test.change_wait_time_after_write(2.5)

    assert under_test.wait_write == 2.5


def test_wait_field_detected(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.wait_for_field")

    under_test.wait_field_detected()

    Emulator.wait_for_field.assert_called_once()


def test_wait_until_string(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    txt = under_test.wait_until_string("abc")

    assert txt == "abc"


def test_wait_until_string_string_not_found(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='String "def" not found in 1 seconds'):
        under_test.wait_until_string("def", 1)


def test_wait_until_string_not_found_until_timeout(
    mocker: MockerFixture, under_test: x3270
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")
    mocker.patch("time.ctime", return_value="Sat Feb 12 15:29:51 2022")

    with pytest.raises(Exception, match='String "abc" not found in 5 seconds'):
        under_test.wait_until_string("abc")
