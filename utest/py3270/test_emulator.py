import errno
import os

import pytest

from Mainframe3270.py3270 import Emulator, TerminatedError

CURDIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def mock_windows(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "nt")


@pytest.fixture
def mock_posix(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "posix")
    mocker.patch("subprocess.Popen")


def test_emulator_default_args(mock_windows):
    under_test = Emulator()

    assert under_test.app.executable == "ws3270"
    assert under_test.app.args == ["-xrm", "ws3270.unlockDelay: False"]


def test_emulator_visible(mock_windows):
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "wc3270"
    assert under_test.app.args == [
        "-xrm",
        "wc3270.unlockDelay: False",
        "-xrm",
        "wc3270.model: 2",
    ]


def test_emulator_none_windows(mock_posix):
    under_test = Emulator()

    assert under_test.app.executable == "s3270"


def test_emulator_none_windows_visible(mock_posix):
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "x3270"


def test_exec_command_when_is_terminated(mock_windows, mocker):
    under_test = Emulator()
    under_test.is_terminated = True

    with pytest.raises(
        TerminatedError, match="This Emulator instance has been terminated"
    ):
        under_test.exec_command(b"abc")


def test_terminate_BrokenPipeError(mock_windows, mocker):
    mocker.patch("Mainframe3270.py3270.ExecutableAppWin.close")
    mocker.patch(
        "Mainframe3270.py3270.Emulator.exec_command", side_effect=BrokenPipeError
    )
    under_test = Emulator()

    under_test.terminate()

    assert under_test.is_terminated


def test_terminate_socket_error(mock_windows, mocker):
    mock_os_error = OSError()
    mock_os_error.errno = errno.ECONNRESET
    mocker.patch("Mainframe3270.py3270.ExecutableAppWin.close")
    mocker.patch(
        "Mainframe3270.py3270.Emulator.exec_command", side_effect=mock_os_error
    )
    under_test = Emulator()

    under_test.terminate()

    under_test.is_terminated = True


def test_terminate_other_socket_error(mock_windows, mocker):
    mocker.patch("Mainframe3270.py3270.ExecutableAppWin.close")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command", side_effect=OSError)
    under_test = Emulator()

    with pytest.raises(OSError):
        under_test.terminate()


def test_is_connected(mock_windows, mocker):
    mocker.patch("Mainframe3270.py3270.ExecutableAppWin.write")
    mocker.patch(
        "Mainframe3270.py3270.ExecutableAppWin.readline",
        side_effect=[
            b"data: abc",
            b"U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000",
            b"ok",
        ],
    )
    under_test = Emulator()

    assert under_test.is_connected()


def test_is_not_connected(mock_windows, mocker):
    mocker.patch("Mainframe3270.py3270.ExecutableAppWin.write")
    mocker.patch(
        "Mainframe3270.py3270.ExecutableAppWin.readline",
        side_effect=[
            b"data: abc",
            b"U U U N C 4 43 80 4 24 0x0 0.000",
            b"ok",
        ],
    )
    under_test = Emulator()

    assert not under_test.is_connected()


def test_is_connected_NotConnectedException(mock_windows):
    under_test = Emulator()

    assert not under_test.is_connected()
