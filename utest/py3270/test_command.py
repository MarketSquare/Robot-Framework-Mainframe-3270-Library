import warnings

import pytest
from pytest_mock import MockerFixture

# fmt: off
from Mainframe3270.py3270 import (Command, CommandError, Emulator, s3270App,
                                  wc3270App, ws3270App, x3270App)

# fmt: on


def test_command_default(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
    app = Emulator()

    under_test = Command(app, b"abc")

    assert under_test.app == app
    assert under_test.cmdstr == b"abc"
    assert under_test.status_line is None
    assert under_test.data == []


def test_command_with_text_type(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
    mocker.patch("warnings.warn")
    app = Emulator()

    under_test = Command(app, "abc")

    warnings.warn.assert_called_with("Commands should be byte strings", stacklevel=3)
    assert isinstance(under_test.cmdstr, bytes)


def test_execute(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
    mocker.patch(
        "Mainframe3270.py3270.ExecutableApp.readline",
        side_effect=[
            b"data: abc",
            b"U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000",
            b"ok",
        ],
    )
    app = x3270App()
    under_test = Command(app, b"abc")

    under_test.execute()

    assert under_test.data == [b"abc"]


def test_handle_result_quit(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
    mocker.patch("Mainframe3270.py3270.ExecutableApp.readline", return_value=b"")
    app = x3270App()
    under_test = Command(app, b"Quit")

    under_test.execute()


def test_handle_result_error(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
    mocker.patch("Mainframe3270.py3270.ExecutableApp.readline", return_value=b"error")
    app = s3270App()
    under_test = Command(app, b"abc")

    with pytest.raises(CommandError, match="[no data message]"):
        under_test.execute()


def test_handle_result_with_data(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
    mocker.patch(
        "Mainframe3270.py3270.ExecutableApp.readline",
        side_effect=[
            b"data: abc",
            b"U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000",
            b"error",
        ],
    )
    app = ws3270App()
    under_test = Command(app, b"abc")

    with pytest.raises(CommandError, match="abc"):
        under_test.execute()


def test_handle_result_not_ok_or_error(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.wc3270App.readline", return_value=b"abc")
    mocker.patch("Mainframe3270.py3270.wc3270App.write")
    app = wc3270App()
    under_test = Command(app, b"abc")

    with pytest.raises(
        ValueError, match='expected "ok" or "error" result, but received: abc'
    ):
        under_test.execute()
