import errno

import pytest
from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator, TerminatedError


@pytest.mark.usefixtures("mock_windows")
def test_emulator_default_args():
    under_test = Emulator()

    assert under_test.app.executable == "ws3270"
    assert under_test.app.args == ["-xrm", "ws3270.unlockDelay: False"]


@pytest.mark.usefixtures("mock_windows")
def test_emulator_visible():
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "wc3270"
    assert under_test.app.args == [
        "-xrm",
        "wc3270.unlockDelay: False",
        "-xrm",
        "wc3270.model: 2",
    ]


@pytest.mark.usefixtures("mock_posix")
def test_emulator_none_windows():
    under_test = Emulator()

    assert under_test.app.executable == "s3270"


@pytest.mark.usefixtures("mock_posix")
def test_emulator_none_windows_visible():
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "x3270"


@pytest.mark.usefixtures("mock_windows")
def test_emulator_with_extra_args():
    extra_args = ["-cadir", "/path/to/ca_dir"]
    under_test = Emulator(extra_args=extra_args)

    assert all(arg in under_test.app.args for arg in extra_args)
    assert under_test.app.args > extra_args


@pytest.mark.usefixtures("mock_windows")
def test_exec_command_when_is_terminated():
    under_test = Emulator()
    under_test.is_terminated = True

    with pytest.raises(
        TerminatedError, match="This Emulator instance has been terminated"
    ):
        under_test.exec_command(b"abc")


@pytest.mark.usefixtures("mock_windows")
def test_terminate_BrokenPipeError(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.close")
    mocker.patch(
        "Mainframe3270.py3270.Emulator.exec_command", side_effect=BrokenPipeError
    )
    under_test = Emulator()

    under_test.terminate()

    assert under_test.is_terminated


@pytest.mark.usefixtures("mock_windows")
def test_terminate_socket_error(mocker: MockerFixture):
    mock_os_error = OSError()
    mock_os_error.errno = errno.ECONNRESET
    mocker.patch("Mainframe3270.py3270.wc3270App.close")
    mocker.patch(
        "Mainframe3270.py3270.Emulator.exec_command", side_effect=mock_os_error
    )
    under_test = Emulator()

    under_test.terminate()

    under_test.is_terminated = True


@pytest.mark.usefixtures("mock_windows")
def test_terminate_other_socket_error(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.close")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command", side_effect=OSError)
    under_test = Emulator()

    with pytest.raises(OSError):
        under_test.terminate()


@pytest.mark.usefixtures("mock_windows")
def test_is_connected(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.write")
    mocker.patch(
        "Mainframe3270.py3270.wc3270App.readline",
        side_effect=[
            b"data: abc",
            b"U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000",
            b"ok",
        ],
    )
    under_test = Emulator(True)

    assert under_test.is_connected()


@pytest.mark.usefixtures("mock_windows")
def test_is_not_connected(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.write")
    mocker.patch(
        "Mainframe3270.py3270.wc3270App.readline",
        side_effect=[
            b"data: abc",
            b"U U U N C 4 43 80 4 24 0x0 0.000",
            b"ok",
        ],
    )
    under_test = Emulator(True)

    assert not under_test.is_connected()


@pytest.mark.usefixtures("mock_windows")
def test_is_connected_NotConnectedException():
    under_test = Emulator(True)

    assert not under_test.is_connected()


@pytest.mark.usefixtures("mock_windows")
def test_string_get(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.write")
    mocker.patch(
        "Mainframe3270.py3270.wc3270App.readline",
        side_effect=[
            b"data: Welcome to PUB400.COM * your public IBM i server",
            b"U U U C(pub400.com) C 4 43 80 0 56 0x1a00169 0.000",
            b"ok",
        ],
    )
    under_test = Emulator(True)

    string = under_test.string_get(1, 10, 48)

    assert string == "Welcome to PUB400.COM * your public IBM i server"


@pytest.mark.usefixtures("mock_windows")
def test_string_get_calls__check_limits(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator._check_limits")
    mocker.patch("Mainframe3270.py3270.wc3270App.write")
    mocker.patch(
        "Mainframe3270.py3270.wc3270App.readline",
        side_effect=[
            b"data: Welcome to PUB400.COM * your public IBM i server",
            b"U U U C(pub400.com) C 4 43 80 0 56 0x1a00169 0.000",
            b"ok",
        ],
    )
    under_test = Emulator(True)

    under_test.string_get(1, 10, 48)

    Emulator._check_limits.assert_called_with(1, 10)


@pytest.mark.usefixtures("mock_windows")
def test_string_get_exceeds_x_axis(mocker: MockerFixture):
    under_test = Emulator(True)

    with pytest.raises(
        Exception, match="You have exceeded the x-axis limit of the mainframe screen"
    ):
        under_test.string_get(1, 10, 72)


@pytest.mark.usefixtures("mock_windows")
def test_search_string(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")
    under_test = Emulator()

    assert under_test.search_string("abc")


@pytest.mark.usefixtures("mock_windows")
def test_search_string_returns_False(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")
    under_test = Emulator()

    assert not under_test.search_string("def")


@pytest.mark.usefixtures("mock_windows")
def test_search_string_ignoring_case(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="ABC")
    under_test = Emulator()

    assert under_test.search_string("abc", True)


@pytest.mark.usefixtures("mock_windows")
def test_read_all_screen(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")
    under_test = Emulator()

    content = under_test.read_all_screen()

    assert content == "a" * 24


@pytest.mark.usefixtures("mock_windows")
def test_check_limits():
    under_test = Emulator()

    under_test._check_limits(24, 80)


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(
    ("ypos", "xpos", "expected_error"),
    [
        (25, 80, "You have exceeded the y-axis limit of the mainframe screen"),
        (24, 81, "You have exceeded the x-axis limit of the mainframe screen"),
    ],
)
def test_check_limits_raises_Exception(ypos, xpos, expected_error):
    under_test = Emulator()

    with pytest.raises(Exception, match=expected_error):
        under_test._check_limits(ypos, xpos)
