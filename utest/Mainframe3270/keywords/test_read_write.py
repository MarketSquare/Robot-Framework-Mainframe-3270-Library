import pytest
from pytest_mock import MockerFixture

from Mainframe3270.keywords.read_write import ReadWriteKeywords
from Mainframe3270.py3270 import Emulator

from .utils import create_test_object_for


@pytest.fixture
def under_test():
    return create_test_object_for(ReadWriteKeywords)


def test_read(under_test: ReadWriteKeywords, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    string = under_test.read(1, 1, 3)

    Emulator.string_get.assert_called_once_with(1, 1, 3)
    assert string == "abc"


def test_read_all_screen(under_test: ReadWriteKeywords, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.read_all_screen", return_value="all screen")

    content = under_test.read_all_screen()

    Emulator.read_all_screen.assert_called_once()
    assert content == "all screen"


def test_write(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write("abc")

    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_called_once()


def test_write_bare(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_bare("abc")

    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_not_called()


def test_write_in_position(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_in_position("abc", 5, 5)

    Emulator.move_to.assert_called_once_with(5, 5)
    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_called_once()


def test_write_bare_in_position(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_bare_in_position("abc", 5, 5)

    Emulator.move_to.assert_called_once_with(5, 5)
    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_not_called()


def test_find_string(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.find_string", return_value=[(5, 10)])

    assert under_test.find_string("abc") == [(5, 10)]

    Emulator.find_string.assert_called_once_with("abc", False)


def test_find_string_ignore_case(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.find_string", return_value=[(5, 10)])

    assert under_test.find_string("abc", ignore_case=True) == [(5, 10)]

    Emulator.find_string.assert_called_once_with("abc", True)
