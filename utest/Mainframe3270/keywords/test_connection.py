import os
from unittest.mock import mock_open, patch

import pytest
from pytest_mock import MockerFixture
from robot.api import logger
from robot.utils import ConnectionCache

from Mainframe3270.keywords import ConnectionKeywords
from Mainframe3270.py3270 import Emulator

from .utils import create_test_object_for

CURDIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def under_test():
    return create_test_object_for(ConnectionKeywords)


def test_open_connection(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register")

    under_test.open_connection("myhost")

    Emulator.connect.assert_called_with("myhost:23")
    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] is None


def test_open_connection_with_alias(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register")

    under_test.open_connection("myhost", alias="myalias")

    Emulator.connect.assert_called_with("myhost:23")
    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] == "myalias"


def test_open_connection_returns_index(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register", return_value=1)

    index = under_test.open_connection("myhost", alias="myalias")

    assert index == 1


def test_open_connection_with_lu(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")

    under_test.open_connection("myhost", "lu")

    Emulator.connect.assert_called_with("lu@myhost:23")


def test_open_connection_with_port(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")

    under_test.open_connection("myhost", port=2222)

    Emulator.connect.assert_called_with("myhost:2222")


def test_open_connection_with_extra_args(mocker: MockerFixture, under_test: ConnectionKeywords):
    extra_args = ["-xrm", "*blankFill: true"]
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    mocker.patch("Mainframe3270.py3270.Emulator.connect")

    under_test.open_connection("myhost", extra_args=extra_args)

    Emulator.__init__.assert_called_with(True, 30.0, extra_args, "2")


def test_open_connection_with_port_from_argument_and_from_extra_args(
    mocker: MockerFixture, under_test: ConnectionKeywords
):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.api.logger.warn")

    under_test.open_connection("myhost", port=12345, extra_args=["-port", "12345"])

    logger.warn.assert_called_with(
        "The connection port has been specified both in the `port` argument and in `extra_args`. "
        "The port specified in `extra_args` will take precedence over the `port` argument. "
        "To avoid this warning, you can either remove the port command-line option from `extra_args`, "
        "or leave the `port` argument at its default value of 23."
    )


def test_open_connection_with_default_model(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    mocker.patch("Mainframe3270.py3270.Emulator.connect")

    under_test.open_connection("myhost")

    Emulator.__init__.assert_called_with(True, 30.0, [], "2")


def test_open_connection_with_model_from_extra_args(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    model = "4"
    extra_args = ["-xrm", f"*model: {model}"]

    under_test.open_connection("myhost", extra_args=extra_args)

    Emulator.__init__.assert_called_with(True, 30.0, extra_args, model)


def test_process_args_returns_empty_list(under_test: ConnectionKeywords):
    args = None

    processed_args = under_test._process_args(args)

    assert processed_args == []


def test_process_args_from_list(under_test: ConnectionKeywords):
    args = ["-xrm", "wc3270.acceptHostname: myhost.com"]

    processed_args = under_test._process_args(args)

    assert processed_args == args


def test_process_args_from_file_oneline(under_test: ConnectionKeywords):
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


def test_process_args_from_multiline_file(under_test: ConnectionKeywords):
    args = os.path.join(CURDIR, "resources", "argfile_multiline.txt")

    processed_args = under_test._process_args(args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    assert processed_args == args_from_file


def test_process_args_from_multiline_file_with_comments(under_test: ConnectionKeywords):
    args = os.path.join(CURDIR, "resources", "argfile_multiline_comments.txt")

    processed_args = under_test._process_args(args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    assert processed_args == args_from_file


@pytest.mark.parametrize(
    ("model_arg", "expected_model"),
    [
        (["-xrm", "wc3270.model: 2"], "2"),
        (["-xrm", "ws3270.model: 2"], "2"),
        (["-xrm", "x3270.model: 2"], "2"),
        (["-xrm", "s3270.model: 2"], "2"),
        (["-xrm", "*model: 2"], "2"),
        (["-xrm", "*model:2"], "2"),
        (["-xrm", "*model:3"], "3"),
        (["-xrm", "*model:4"], "4"),
        (["-xrm", "*model:5"], "5"),
        (["-xrm", "*model:3278-2"], "3278-2"),
        (["-xrm", "*model:3278-2-E"], "3278-2-E"),
        (["-xrm", "*model:3279-2"], "3279-2"),
        (["-xrm", "*model:3279-2-E"], "3279-2-E"),
        (["-xrm", "*model:3278-3"], "3278-3"),
        (["-xrm", "*model:3278-3-E"], "3278-3-E"),
        (["-xrm", "*model:3279-3"], "3279-3"),
        (["-xrm", "*model:3279-3-E"], "3279-3-E"),
        (["-xrm", "*model:3278-4"], "3278-4"),
        (["-xrm", "*model:3278-4-E"], "3278-4-E"),
        (["-xrm", "*model:3279-4"], "3279-4"),
        (["-xrm", "*model:3279-4-E"], "3279-4-E"),
        (["-xrm", "*model:3278-5"], "3278-5"),
        (["-xrm", "*model:3278-5-E"], "3278-5-E"),
        (["-xrm", "*model:3279-5"], "3279-5"),
        (["-xrm", "*model:3279-5-E"], "3279-5-E"),
    ],
)
def test_get_model_from_list_or_file_with_list(under_test: ConnectionKeywords, model_arg: list, expected_model: str):
    model = under_test._get_model_from_list_or_file(model_arg)

    assert model == expected_model


def test_get_model_from_list_or_file_with_file(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    with patch("builtins.open", mock_open(read_data="*hostname: pub400.com\n*model: 5")):
        model = under_test._get_model_from_list_or_file("session.x3270")

        assert model == "5"


def test_get_model_from_list_or_file_returns_None(under_test: ConnectionKeywords):
    assert under_test._get_model_from_list_or_file([]) is None
    assert under_test._get_model_from_list_or_file(None) is None


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
def test_port_in_extra_args(args: list, expected: bool, under_test: ConnectionKeywords):
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
    mocker: MockerFixture,
    os_name: str,
    under_test: ConnectionKeywords,
    visible: bool,
    expected: str,
):
    mocker.patch("Mainframe3270.keywords.connection.os_name", os_name)
    under_test.visible = visible

    with pytest.raises(
        ValueError,
        match=f"Based on the emulator that you are using, "
        f'the session file extension has to be ".{expected}", but it was ".txt"',
    ):
        under_test._check_session_file_extension("file_with_wrong_extension.txt")


def test_contains_hostname_raises_ValueError(under_test: ConnectionKeywords):
    with patch("builtins.open", mock_open(read_data="wc3270.port: 992\n")):
        with pytest.raises(
            ValueError,
            match="Your session file needs to specify the hostname resource to set up the connection",
        ):
            under_test._check_contains_hostname("wc3270.session")


@pytest.mark.parametrize(
    ("os_name", "visible"),
    [
        ("nt", False),
        ("posix", True),
        ("posix", False),
    ],
)
def test_open_connection_from_session_file_uses_default_model(
    under_test: ConnectionKeywords, os_name: str, visible: bool, mocker: MockerFixture
):
    mocker.patch("Mainframe3270.keywords.connection.os_name", os_name)
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    under_test.visible = visible

    with patch("builtins.open", mock_open(read_data="*hostname: pub400.com")):
        under_test.open_connection_from_session_file("session.s3270")

        Emulator.__init__.assert_called_with(visible, 30.0, ["session.s3270"], "2")


def test_open_connection_from_session_file_uses_default_model_for_wc3270(
    mocker: MockerFixture, under_test: ConnectionKeywords
):
    mocker.patch("Mainframe3270.keywords.connection.os_name", "nt")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test.visible = True
    with patch("builtins.open", mock_open(read_data="*hostname: pub400.com")):
        under_test.open_connection_from_session_file("session.s3270")

        Emulator.__init__.assert_called_with(True, 30.0, model="2")


@pytest.mark.parametrize(
    ("os_name", "visible"),
    [
        ("nt", False),
        ("posix", True),
        ("posix", False),
    ],
)
def test_open_connection_from_session_file_uses_model_from_file(
    mocker: MockerFixture, os_name: str, visible: bool, under_test: ConnectionKeywords
):
    mocker.patch("Mainframe3270.keywords.connection.os_name", os_name)
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    under_test.visible = visible

    with patch("builtins.open", mock_open(read_data="*hostname: pub400.com\n*model: 5")):
        under_test.open_connection_from_session_file("session.x3270")

        Emulator.__init__.assert_called_with(visible, 30.0, ["session.x3270"], "5")


def test_open_connection_from_session_file_uses_model_from_file_for_wc3270(
    mocker: MockerFixture, under_test: ConnectionKeywords
):
    mocker.patch("Mainframe3270.keywords.connection.os_name", "nt")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.py3270.Emulator.__init__", return_value=None)
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test.visible = True
    with patch("builtins.open", mock_open(read_data="*hostname: pub400.com\nwc3270.model: 5")):
        under_test.open_connection_from_session_file("session.wc3270")

        Emulator.__init__.assert_called_with(True, 30.0, model="5")


def test_open_connection_from_session_file_registers_connection(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_contains_hostname")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._get_model_from_list_or_file", return_value="2")
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register")

    under_test.open_connection_from_session_file("session.wc3270")

    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] is None


def test_open_connection_from_session_file_registers_connection_with_alias(
    mocker: MockerFixture, under_test: ConnectionKeywords
):
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_contains_hostname")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._get_model_from_list_or_file", return_value="3")
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register")

    under_test.open_connection_from_session_file("session.wc3270", "myalias")

    assert isinstance(ConnectionCache.register.call_args[0][0], Emulator)
    assert ConnectionCache.register.call_args[0][1] == "myalias"


def test_open_connection_from_session_file_returns_index(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_session_file_extension")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._check_contains_hostname")
    mocker.patch("Mainframe3270.keywords.ConnectionKeywords._get_model_from_list_or_file", return_value="4")
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("robot.utils.ConnectionCache.register", return_value=1)

    index = under_test.open_connection_from_session_file("session.wc3270")

    assert index == 1


def test_switch_connection(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("robot.utils.ConnectionCache.switch")

    under_test.switch_connection(1)
    ConnectionCache.switch.assert_called_with(1)

    under_test.switch_connection("myalias")
    ConnectionCache.switch.assert_called_with("myalias")


def test_close_connection(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate")

    under_test.close_connection()

    Emulator.terminate.assert_called_once()


def test_close_all_connections(mocker: MockerFixture, under_test: ConnectionKeywords):
    mocker.patch("robot.utils.ConnectionCache.close_all")

    under_test.close_all_connections()

    ConnectionCache.close_all.assert_called_with("terminate")
