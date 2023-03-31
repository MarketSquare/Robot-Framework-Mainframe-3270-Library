import os
import re
import socket
from unittest.mock import mock_open, patch

import pytest
from pytest_mock import MockerFixture

import Mainframe3270
from Mainframe3270 import x3270
from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import X3270

from .conftest import X3270_DEFAULT_ARGS

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_open_connection(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost")

    m_connect.assert_called_with("myhost:23")


def test_open_connection_existing_emulator(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("Mainframe3270.X3270.close_connection")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.mf = Emulator()

    under_test.open_connection("myhost")

    Mainframe3270.X3270.close_connection.assert_called()


def test_open_connection_with_lu(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", "lu")

    m_connect.assert_called_with("lu@myhost:23")


def test_open_connection_with_port(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", port=2222)

    m_connect.assert_called_with("myhost:2222")


def test_open_connection_with_port_from_argument_and_from_extra_args(
    mocker: MockerFixture,
):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    m_logger = mocker.patch("robot.api.logger.warn")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", port=12345, extra_args=["-port", "12345"])

    m_logger.assert_called_with(
        "The connection port has been specified both in the `port` argument and in `extra_args`. "
        "The port specified in `extra_args` will take precedence over the `port` argument. "
        "To avoid this warning, you can either remove the port command-line option from `extra_args`, "
        "or leave the `port` argument at its default value of 23."
    )


def test_open_connection_with_extra_args_oneline(mocker: MockerFixture):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources", "argfile_oneline.txt")

    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = [
        "-charset",
        "german",
        "-xrm",
        "*acceptHostname: myhost.com",
        "-xrm",
        "*blankFill: true",
    ]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


@pytest.mark.usefixtures("mock_posix")
def test_open_connection_none_windows_extra_args_oneline(mocker: MockerFixture):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources", "argfile_oneline.txt")

    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = [
        "-charset",
        "german",
        "-xrm",
        "*acceptHostname: myhost.com",
        "-xrm",
        "*blankFill: true",
    ]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


@pytest.mark.usefixtures("mock_windows")
def test_open_connection_with_extra_args_multiline(mocker: MockerFixture):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources", "argfile_multiline.txt")

    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


@pytest.mark.usefixtures("mock_windows")
def test_open_connection_with_extra_args_multiline_comments(mocker: MockerFixture):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources", "argfile_multiline_comments.txt")

    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


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


def test_contains_hostname(under_test: X3270):
    session_file = os.path.join(CURDIR, "resources", "session.wc3270")
    with pytest.raises(
        ValueError,
        match="Your session file needs to specify the hostname resource to set up the connection",
    ):
        under_test._check_contains_hostname(session_file)


@pytest.mark.parametrize(
    "model",
    [
        "wc3270.model: 2",
        "ws3270.model:2",
        "x3270.model: 2",
        "s3270.model: 2",
        "*model:2",
        "",
    ],
)
def test_check_model(model: str, under_test: X3270):
    with patch("builtins.open", mock_open(read_data=model)) as session_file:
        under_test._check_model(session_file)


@pytest.mark.parametrize(
    ("model_string", "model"),
    [
        ("wc3270.model: 4", "4"),
        ("ws3270.model:4", "4"),
        ("x3270.model: 5", "5"),
        ("s3270.model: 3279-4-E", "3279-4-E"),
        ("*model: 3278-4", "3278-4"),
    ],
)
def test_check_model_raises_ValueError(
    model_string: str, model: SystemError, under_test: X3270
):
    with patch("builtins.open", mock_open(read_data=model_string)) as session_file:
        with pytest.raises(
            ValueError,
            match=re.escape(
                f'Robot-Framework-Mainframe-3270-Library currently only supports model "2", '
                f'the model you specified in your session file was "{model}". '
                f'Please change it to "2", using either the session wizard if you are on Windows, '
                f'or by editing the model resource like this "*model: 2"'
            ),
        ):
            under_test._check_model(session_file)


def test_close_connection(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate")
    under_test.close_connection()

    assert Emulator.terminate.called_once()
    assert under_test.mf is None


def test_close_connection_socket_error(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate", side_effect=socket.error)
    under_test.close_connection()

    assert under_test.mf is None
