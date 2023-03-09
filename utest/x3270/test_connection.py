import os
import socket

import pytest
from pytest_mock import MockerFixture

import Mainframe3270
from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import x3270

from .conftest import X3270_DEFAULT_ARGS

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_open_connection(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost")

    m_connect.assert_called_with("myhost:23")


def test_open_connection_existing_emulator(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("Mainframe3270.x3270.close_connection")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.mf = Emulator()

    under_test.open_connection("myhost")

    Mainframe3270.x3270.close_connection.assert_called()


def test_open_connection_with_lu(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", "lu")

    m_connect.assert_called_with("lu@myhost:23")


def test_open_connection_with_port(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", port=2222)

    m_connect.assert_called_with("myhost:2222")


def test_open_connection_with_port_from_argument_and_from_extra_args(
    mocker: MockerFixture,
):
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    m_logger = mocker.patch("robot.api.logger.warn")
    under_test = x3270(**X3270_DEFAULT_ARGS)
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
    extra_args = os.path.join(CURDIR, "resources/argfile_oneline.txt")

    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = ["-charset", "german"]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


@pytest.mark.usefixtures("mock_posix")
def test_open_connection_none_windows_extra_args_oneline(
    mock_posix, mocker: MockerFixture
):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources/argfile_oneline.txt")

    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = ["-charset", "german"]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


@pytest.mark.usefixtures("mock_windows")
def test_open_connection_with_extra_args_multiline(mocker: MockerFixture):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources/argfile_multiline.txt")

    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


@pytest.mark.usefixtures("mock_windows")
def test_open_connection_with_extra_args_multiline_comments(mocker: MockerFixture):
    m_emulator = mocker.patch(
        "Mainframe3270.py3270.Emulator.__init__", return_value=None
    )
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    extra_args = os.path.join(CURDIR, "resources/argfile_multiline_comments.txt")

    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", extra_args=extra_args)

    args_from_file = ["-charset", "bracket", "-accepthostname", "myhost.com"]
    m_emulator.assert_called_with(True, 30.0, args_from_file)


def test_close_connection(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate")
    under_test.close_connection()

    assert Emulator.terminate.called_once()
    assert under_test.mf is None


def test_close_connection_socket_error(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate", side_effect=socket.error)
    under_test.close_connection()

    assert under_test.mf is None
