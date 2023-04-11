import time

from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import X3270

from .conftest import X3270_DEFAULT_ARGS


def test_execute_command(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("time.sleep")
    under_test.execute_command("cmd")

    Emulator.exec_command.assert_called_with("cmd".encode("utf-8"))
    time.sleep.assert_called_with(under_test.wait)


def test_delete_char(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.delete_char()

    Emulator.move_to.assert_not_called()
    Emulator.exec_command.assert_called_with(b"Delete")


def test_delete_char_in_position(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.delete_char(5, 5)

    Emulator.move_to.assert_called_with(5, 5)
    Emulator.exec_command.assert_called_with(b"Delete")


def test_delete_field(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.delete_field()

    Emulator.move_to.assert_not_called()
    Emulator.exec_command.assert_called_with(b"DeleteField")


def test_delete_field_in_position(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.delete_field(5, 5)

    Emulator.move_to.assert_called_with(5, 5)
    Emulator.exec_command.assert_called_with(b"DeleteField")


def test_send_enter(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")
    mocker.patch("time.sleep")

    under_test.send_enter()

    Emulator.send_enter.assert_called_once()
    time.sleep.assert_called_once_with(X3270_DEFAULT_ARGS["wait_time"])


def test_move_next_field(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.move_next_field()

    Emulator.exec_command.assert_called_with(b"Tab")


def test_move_previous_field(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.move_previous_field()

    Emulator.exec_command.assert_called_with(b"BackTab")


def test_send_pf(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")

    under_test.send_PF("5")

    Emulator.exec_command.assert_called_with("PF(5)".encode("utf-8"))
