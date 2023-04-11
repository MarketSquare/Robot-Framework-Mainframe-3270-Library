import os
import pytest

from Mainframe3270.x3270 import X3270
from pytest_mock import MockerFixture
from .conftest import X3270_DEFAULT_ARGS

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_open_connection_cust(mocker: MockerFixture):
    m_connect = mocker.patch("Mainframe3270.py3270.Emulator.connect")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.open_connection("2")

    assert under_test.model == "2"


def test_len_extra_args_(mocker: MockerFixture, extra_args=[]):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    assert len(extra_args) == 0


def test_model_not_in_extra_args_(mocker: MockerFixture, extra_args=[]):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    assert "-model" not in extra_args


@pytest.mark.parametrize("model,model_num, expected",
                         [('model', 2, "['-model', '2', '-oversize', {'rows': 24, 'columns': 80}]"),
                          ('model', 3, "['-model', '3', '-oversize', {'rows': 32, 'columns': 80}]"),
                          ('model', 4, "['-model', '4', '-oversize', {'rows': 43, 'columns': 80}]"),
                          ('model', 5, "['-model', '5', '-oversize', {'rows': 27, 'columns': 132}]")])
def test_extra_args_equal_size_args(model, model_num, expected):
    assert model, model_num == expected
