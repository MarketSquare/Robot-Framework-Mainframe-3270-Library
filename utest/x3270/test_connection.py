import socket

from pytest_mock import MockerFixture

import Mainframe3270
from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import x3270

from .conftest import X3270_DEFAULT_ARGS


def test_open_connection(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost")

    m_connect.assert_called_with("myhost:23")


def test_open_connection_existing_emulator(mocker):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    mocker.patch("Mainframe3270.py3270.Emulator.connect")
    mocker.patch("Mainframe3270.x3270.close_connection")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.mf = Emulator()

    under_test.open_connection("myhost")

    Mainframe3270.x3270.close_connection.assert_called()


def test_open_connection_with_lu(mocker):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", "lu")

    m_connect.assert_called_with("lu@myhost:23")


def test_open_connection_with_port(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("myhost", port=2222)

    m_connect.assert_called_with("myhost:2222")


def test_close_connection(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate")
    under_test.close_connection()

    assert Emulator.terminate.called_once()
    assert under_test.mf is None


def test_close_connection_socket_error(mocker: MockerFixture, under_test: x3270):
    mocker.patch("Mainframe3270.py3270.Emulator.terminate", side_effect=socket.error)
    under_test.close_connection()

    assert under_test.mf is None
