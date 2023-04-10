from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import X3270


def test_write(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write("abc")

    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_called_once()


def test_write_bare(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_bare("abc")

    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_not_called()


def test_write_in_position(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_in_position("abc", 5, 5)

    Emulator.move_to.assert_called_once_with(5, 5)
    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_called_once()


def test_write_bare_in_position(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_bare_in_position("abc", 5, 5)

    Emulator.move_to.assert_called_once_with(5, 5)
    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_not_called()
