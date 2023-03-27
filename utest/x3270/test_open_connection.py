import socket
import os
import Mainframe3270
import pytest

from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import x3270
from typing import Any, List, Optional, Union
from pytest_mock import MockerFixture

from .conftest import X3270_DEFAULT_ARGS

CURDIR = os.path.dirname(os.path.realpath(__file__))


# check height and width arguments
def test_open_connection_cust(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = x3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection(24, 80)

    assert under_test.height == 24
    assert under_test.width == 80


# check if length of extra_args is equal to 0
def test_len_extra_args_(mocker: MockerFixture, extra_args=[]):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    assert len(extra_args) == 0


# check if "-model" not present in extra_args
def test_model_not_in_extra_args_(mocker: MockerFixture, extra_args=[]):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    assert "-model" not in extra_args


# check if extra_args is equal to size_args
@pytest.mark.parametrize("_height,_width,expected", [(24, 80, "['-model', '2', '-oversize', '80x24']"),
                                                     (32, 80, "['-model', '3', '-oversize', '80x32']"),
                                                     (43, 80, "['-model', '4', '-oversize', '80x43']"),
                                                     (27, 132, "['-model', '5', '-oversize', '132x27']")])
def test_extra_args_equal_size_args(mocker: MockerFixture, _height, _width, expected):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    assert _height, _width == expected
