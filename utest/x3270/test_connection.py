import os
import re
from unittest.mock import mock_open, patch

import pytest
from pytest_mock import MockerFixture
from robot.api import logger
from robot.utils import ConnectionCache

from Mainframe3270 import x3270
from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import X3270

from .conftest import X3270_DEFAULT_ARGS

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_open_connection(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost")

    Emulator.connect.assert_called_with("myhost:23")
    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] is None


def test_open_connection_with_alias(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", alias="myalias")

    Emulator.connect.assert_called_with("myhost:23")
    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] == "myalias"


def test_open_connection_returns_index(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register", return_value=1)
    under_test = X3270(**X3270_DEFAULT_ARGS)
    index = under_test.open_connection("myhost", alias="myalias")

    assert index == 1


def test_open_connection_with_lu(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", "lu")

    Emulator.connect.assert_called_with("lu@myhost:23")


def test_open_connection_with_port(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", port=2222)

    Emulator.connect.assert_called_with("myhost:2222")


def test_open_connection_with_extra_args(mocker: MockerFixture, under_test: X3270):
    extra_args = ["-xrm", "*blankFill: true"]
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test.open_connection("myhost", extra_args=extra_args)

    Emulator.__init__.assert_called_with(True, 30.0, extra_args, "2")


def test_open_connection_with_port_from_argument_and_from_extra_args(
    mocker: MockerFixture,
):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.api.logger.warn")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", port=12345, extra_args=["-port", "12345"])

    logger.warn.assert_called_with(
        "The connection port has been specified both in the `port` argument and in `extra_args`. "
        "The port specified in `extra_args` will take precedence over the `port` argument. "
        "To avoid this warning, you can either remove the port command-line option from `extra_args`, "
        "or leave the `port` argument at its default value of 23."
    )


def test_process_args_returns_empty_list(under_test: X3270):
    args = None
    processed_args = under_test._process_args(args)

    assert processed_args == []


def test_process_args_from_list(under_test: X3270):
    args = ["-xrm", "wc3270.acceptHostname: myhost.com"]
    processed_args = under_test._process_args(args)

    assert processed_args == args


def test_process_args_from_file_oneline(under_test: X3270):
    args = os.path.join(CURDIR, "resources", "argfile_oneline.txt")
    processed_args = under_test._process_args(args)

    args_from_file = [
        "-charset",
        "german",
        "-xrm",
        "*acceptHostname: myhost.com",
        "-xrm",
        "*blankFill: true",
    ]
    assert processed_args == args_from_file


def test_process_args_from_multiline_file(under_test: X3270):
    args = os.path.join(CURDIR, "resources", "argfile_multiline.txt")
    processed_args = under_test._process_args(args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    assert processed_args == args_from_file


def test_process_args_from_multiline_file_with_comments(under_test: X3270):
    args = os.path.join(CURDIR, "resources", "argfile_multiline_comments.txt")
    with open(args) as f:
        print(f.read())
    processed_args = under_test._process_args(args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    assert processed_args == args_from_file


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (["-xrm", "x3270.port: 992"], True),
        (["-xrm", "s3270.port: 992"], True),
        (["-xrm", "wc3270.port:992"], True),
        (["-xrm", "ws3270.port: 992"], True),
        (["-xrm", "*port: 992"], True),
        (["-port", "992"], True),
        (["-scriptport", "9999"], False),
        (["-xrm", "wc3270.scriptPort: 992"], False),
        ([], False),
    ],
)
def test_port_in_extra_args(args: list, expected: bool, under_test: X3270):
    port_in_extra_args = under_test._port_in_extra_args(args)

    assert port_in_extra_args == expected


@pytest.mark.parametrize(
    ("os_name, visible, expected"),
    [
        ("nt", True, "wc3270"),
        ("nt", False, "ws3270"),
        ("posix", True, "x3270"),
        ("posix", False, "s3270"),
    ],
)
def test_check_session_file_extension(
    os_name: str,
    under_test: X3270,
    visible: bool,
    expected: str,
):
    x3270.os_name = os_name
    under_test.visible = visible
    with pytest.raises(
        ValueError,
        match=f"Based on the emulator that you are using, "
        f'the session file extension has to be ".{expected}", but it was ".txt"',
    ):
        under_test._check_session_file_extension("file_with_wrong_extension.txt")


def test_contains_hostname_raises_ValueError(under_test: X3270):
    with patch(
        "builtins.open", mock_open(read_data="wc3270.port: 992\n")
    ) as session_file:
        with pytest.raises(
            ValueError,
            match="Your session file needs to specify the hostname resource to set up the connection",
        ):
            under_test._check_contains_hostname(session_file)


def test_open_connection_from_session_file_registers_connection(
    mocker: MockerFixture, under_test: X3270
):
    mocker.patch("Mainframe3270.x3270.X3270._check_session_file_extension")
    mocker.patch("Mainframe3270.x3270.X3270._check_contains_hostname")
    mocker.patch("robot.utils.ConnectionCache.register")
    under_test.open_connection_from_session_file("session.wc3270")

    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] is None


def test_open_connection_from_session_file_registers_connection_with_alias(
    mocker: MockerFixture, under_test: X3270
):
    mocker.patch("Mainframe3270.x3270.X3270._check_session_file_extension")
    mocker.patch("Mainframe3270.x3270.X3270._check_contains_hostname")
    mocker.patch("robot.utils.ConnectionCache.register")
    under_test.open_connection_from_session_file("session.wc3270", "myalias")

    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] == "myalias"


def test_open_connection_from_session_file_returns_index(
    mocker: MockerFixture, under_test: X3270
):
    mocker.patch("Mainframe3270.x3270.X3270._check_session_file_extension")
    mocker.patch("Mainframe3270.x3270.X3270._check_contains_hostname")
    mocker.patch("robot.utils.ConnectionCache.register", return_value=1)
    index = under_test.open_connection_from_session_file("session.wc3270")

    assert index == 1


def test_switch_connection(mocker: MockerFixture, under_test: X3270):
    mocker.patch("robot.utils.ConnectionCache.switch")

    under_test.switch_connection(1)
    ConnectionCache.switch.assert_called_with(1)

    under_test.switch_connection("myalias")
    ConnectionCache.switch.assert_called_with("myalias")


def test_close_connection(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate")
    under_test.close_connection()

    assert Emulator.terminate.called_once()


def test_close_all_connections(mocker: MockerFixture, under_test: X3270):
    mocker.patch("robot.utils.ConnectionCache.close_all")
    under_test.close_all_connections()

    ConnectionCache.close_all.assert_called_with("terminate")
