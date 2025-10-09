import pytest
from pytest_mock import MockerFixture
from Mainframe3270.keywords import WaitAndTimeoutKeywords
from Mainframe3270.py3270 import Emulator
from .utils import create_test_object_for


@pytest.fixture
def under_test():
    return create_test_object_for(WaitAndTimeoutKeywords)


def test_change_timeout(under_test: WaitAndTimeoutKeywords):
    under_test.change_timeout(5)

    assert under_test.timeout == 5


def test_change_timeout_with_time_string(under_test: WaitAndTimeoutKeywords):
    under_test.change_timeout("2 minutes")

    assert under_test.timeout == 120


def test_change_timeout_with_timer_string(under_test: WaitAndTimeoutKeywords):
    under_test.change_timeout("0:02:00")

    assert under_test.timeout == 120


def test_change_wait_time(under_test: WaitAndTimeoutKeywords):
    under_test.change_wait_time(2.5)

    assert under_test.wait_time == 2.5


def test_change_wait_time_with_time_string(under_test: WaitAndTimeoutKeywords):
    under_test.change_wait_time("500 millis")

    assert under_test.wait_time == 0.5


def test_change_wait_time_with_timer_string(under_test: WaitAndTimeoutKeywords):
    under_test.change_wait_time("00:00:00.500")

    assert under_test.wait_time == 0.5


def test_change_wait_time_after_write(under_test: WaitAndTimeoutKeywords):
    under_test.change_wait_time_after_write(2.5)

    assert under_test.wait_time_after_write == 2.5


def test_change_wait_time_after_write_with_time_string(
    under_test: WaitAndTimeoutKeywords,
):
    under_test.change_wait_time_after_write("1.5")

    assert under_test.wait_time_after_write == 1.5


def test_change_wait_time_after_write_with_timer_string(
    under_test: WaitAndTimeoutKeywords,
):
    under_test.change_wait_time_after_write("0:00:01.500")

    assert under_test.wait_time_after_write == 1.5


def test_wait_field_detected(mocker: MockerFixture, under_test: WaitAndTimeoutKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.wait_for_field")

    under_test.wait_field_detected()

    Emulator.wait_for_field.assert_called_once()


def test_wait_until_string(mocker: MockerFixture, under_test: WaitAndTimeoutKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    txt = under_test.wait_until_string("abc")

    assert txt == "abc"


def test_wait_until_string_string_not_found(mocker: MockerFixture, under_test: WaitAndTimeoutKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='String "def" not found in 1 second'):
        under_test.wait_until_string("def", 1)


def test_wait_until_string_with_time_time_string(mocker: MockerFixture, under_test: WaitAndTimeoutKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='String "def" not found in 500 milliseconds'):
        under_test.wait_until_string("def", "500 millis")


def test_wait_until_string_with_time_timer_string(mocker: MockerFixture, under_test: WaitAndTimeoutKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='String "def" not found in 500 milliseconds'):
        under_test.wait_until_string("def", "00:00:00.500")
