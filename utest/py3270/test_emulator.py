import errno

import pytest
from pytest_mock import MockerFixture

from Mainframe3270 import py3270
from Mainframe3270.py3270 import Command, Emulator, TerminatedError


@pytest.mark.usefixtures("mock_windows")
def test_emulator_default_args():
    under_test = Emulator()

    assert under_test.app.executable == "ws3270"
    assert under_test.app.args == ["-xrm", "ws3270.unlockDelay: False", "-xrm", "*model: 2"]


@pytest.mark.usefixtures("mock_windows")
def test_emulator_visible():
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "wc3270"
    assert under_test.app.args == [
        "-xrm",
        "wc3270.unlockDelay: False",
        "-xrm",
        "*model: 2",
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
def test_emulator_with_model_default_model():
    under_test = Emulator()

    assert under_test.model == "2", 'default model should be "2"'


@pytest.mark.usefixtures("mock_windows")
def test_emulator_with_model():
    under_test = Emulator(model="4")

    assert under_test.model == "4"


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(
    ("os_name", "visible", "model"),
    [
        ("nt", True, "2"),
        ("nt", False, "2"),
        ("nt", True, "3"),
        ("nt", False, "3"),
        ("posix", True, "2"),
        ("posix", False, "2"),
        ("posix", True, "3"),
        ("posix", False, "3"),
    ],
)
def test_emulator_ws3270App_has_model_as_last_arg(visible: bool, os_name: str, model: str):
    py3270.os_name = os_name
    under_test = Emulator(visible, model=model)

    assert under_test.app.args[-2:] == ["-xrm", f"*model: {model}"]


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(
    ("model", "model_dimensions"),
    [
        ("2", {"rows": 24, "columns": 80}),
        ("3", {"rows": 32, "columns": 80}),
        ("4", {"rows": 43, "columns": 80}),
        ("5", {"rows": 27, "columns": 132}),
    ],
)
def test_emulator_sets_model_dimensions(model, model_dimensions):
    under_test = Emulator(model=model)

    assert under_test.model_dimensions == model_dimensions


@pytest.mark.usefixtures("mock_windows")
def test_set_model_dimensions_raises_ValueError():
    under_test = Emulator()

    with pytest.raises(ValueError, match=r"Model should be one of .+, but was 'wrong model'"):
        under_test._set_model_dimensions("wrong model")


@pytest.mark.usefixtures("mock_windows")
def test_exec_command_when_is_terminated():
    under_test = Emulator()
    under_test.is_terminated = True

    with pytest.raises(TerminatedError, match="This Emulator instance has been terminated"):
        under_test.exec_command(b"abc")


@pytest.mark.usefixtures("mock_windows")
def test_terminate_BrokenPipeError(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.close")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command", side_effect=BrokenPipeError)
    under_test = Emulator()

    under_test.terminate()

    assert under_test.is_terminated


@pytest.mark.usefixtures("mock_windows")
def test_terminate_socket_error(mocker: MockerFixture):
    mock_os_error = OSError()
    mock_os_error.errno = errno.ECONNRESET
    mocker.patch("Mainframe3270.py3270.wc3270App.close")
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command", side_effect=mock_os_error)
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
def test_string_get_calls_check_limits(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
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

    Emulator.check_limits.assert_called_with(1, 10)


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(
    ("model", "length"),
    [
        ("2", 72),
        ("3", 72),
        ("4", 72),
        ("5", 124),
    ],
)
def test_string_get_exceeds_x_axis(mocker: MockerFixture, model: str, length: int):
    mocker.patch("Mainframe3270.py3270.wc3270App.readline")
    under_test = Emulator(True, model=model)

    with pytest.raises(Exception, match="You have exceeded the x-axis limit of the mainframe screen"):
        under_test.string_get(1, 10, length)


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

    assert under_test.search_string("aBc", True)


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(("model", "rows", "columns"), [("2", 24, 80), ("3", 32, 80), ("4", 43, 80), ("5", 27, 132)])
def test_search_string_with_different_model_dimensions(mocker: MockerFixture, model: str, rows: int, columns: int):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    under_test = Emulator(model=model)

    under_test.search_string("abc")

    assert Emulator.string_get.call_count == rows
    Emulator.string_get.assert_called_with(rows, 1, columns)


@pytest.mark.usefixtures("mock_windows")
def test_read_all_screen(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")
    under_test = Emulator()

    content = under_test.read_all_screen()

    assert content == "a" * 24


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(("model", "rows", "columns"), [("2", 24, 80), ("3", 32, 80), ("4", 43, 80), ("5", 27, 132)])
def test_read_all_screen_with_different_model_dimensions(mocker: MockerFixture, model: str, rows: int, columns: int):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get")
    under_test = Emulator(model=model)

    under_test.read_all_screen()

    assert Emulator.string_get.call_count == rows
    Emulator.string_get.assert_called_with(rows, 1, columns)


@pytest.mark.usefixtures("mock_windows")
def test_check_limits():
    under_test = Emulator()

    under_test.check_limits(24, 80)


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(
    ("model", "ypos", "xpos", "expected_error"),
    [
        ("2", 25, 80, "You have exceeded the y-axis limit of the mainframe screen"),
        ("3", 33, 80, "You have exceeded the y-axis limit of the mainframe screen"),
        ("4", 44, 80, "You have exceeded the y-axis limit of the mainframe screen"),
        ("5", 28, 80, "You have exceeded the y-axis limit of the mainframe screen"),
        ("2", 24, 81, "You have exceeded the x-axis limit of the mainframe screen"),
        ("3", 32, 81, "You have exceeded the x-axis limit of the mainframe screen"),
        ("4", 43, 81, "You have exceeded the x-axis limit of the mainframe screen"),
        ("5", 27, 133, "You have exceeded the x-axis limit of the mainframe screen"),
    ],
)
def test_check_limits_raises_Exception(model, ypos, xpos, expected_error):
    under_test = Emulator(model=model)

    with pytest.raises(Exception, match=expected_error):
        under_test.check_limits(ypos, xpos)


def test_get_current_cursor_position(mocker: MockerFixture):
    command = Command(None, b"Query(Cursor)")
    command.data = [b"5 5"]
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command", return_value=command)

    under_test = Emulator()

    # result is 1 based, that is why we expect (6, 6)
    assert under_test.get_current_position() == (6, 6)


def test_get_current_cursor_position_returns_unexpected_value(mocker: MockerFixture):
    command = Command(None, b"Query(Cursor)")
    command.data = [b"5 5", b"unexpected"]
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command", return_value=command)

    under_test = Emulator()

    with pytest.raises(Exception, match="Cursor position returned an unexpected value"):
        under_test.get_current_position()


@pytest.mark.usefixtures("mock_windows")
@pytest.mark.parametrize(
    ("model", "index", "expected"),
    [
        ("2", 1, [(1, 2)]),
        ("2", 79, [(1, 80)]),
        ("2", 80, [(2, 1)]),
        ("2", 139, [(2, 60)]),
        ("5", 131, [(1, 132)]),
    ],
)
def test_get_string_positions(mocker: MockerFixture, model, index, expected):
    under_test = Emulator(model=model)
    mocker.patch(
        "Mainframe3270.py3270.Emulator.read_all_screen", return_value=_mock_return_all_screen(under_test, "abc", index)
    )

    assert under_test.get_string_positions("abc") == expected


def test_get_string_positions_ignore_case(mocker: MockerFixture):
    under_test = Emulator()
    mocker.patch(
        "Mainframe3270.py3270.Emulator.read_all_screen", return_value=_mock_return_all_screen(under_test, "ABC", 5)
    )

    assert under_test.get_string_positions("aBc", True) == [(1, 6)]


def test_get_string_positions_without_result(mocker: MockerFixture):
    under_test = Emulator()
    mocker.patch(
        "Mainframe3270.py3270.Emulator.read_all_screen", return_value=_mock_return_all_screen(under_test, "abc", 1)
    )

    assert under_test.get_string_positions("does not exist") == []


def _mock_return_all_screen(emulator: Emulator, insert_string: str, at_index: int):
    base_str = "a" * (emulator.model_dimensions["rows"] * emulator.model_dimensions["columns"])
    return base_str[:at_index] + insert_string + base_str[at_index : -len(insert_string)]
