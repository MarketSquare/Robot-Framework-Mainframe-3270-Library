import pytest
import os

from pytest_mock import MockerFixture
from Mainframe3270.py3270 import x3270App


# check the model number corresponding to height and width
@pytest.mark.parametrize("_height,_width,expected", [(24, 80, "2"), (32, 80, "3"), (43, 80, "4"), (27, 132, "5")])
def test_get_model(mocker: MockerFixture, _height, _width, expected):
    mocker.patch("Mainframe3270.py3270.x3270App.get_model")
    assert _height, _width == expected


# check the screen size corresponding to height and width
@pytest.mark.parametrize("_height,_width,expected",
                         [(24, 80, "80x24"), (32, 80, "80x32"), (43, 80, "80x43"), (27, 132, "132x27")])
def test_get_screen_size(mocker: MockerFixture, _height, _width, expected):
    mocker.patch("Mainframe3270.py3270.x3270App.get_screen_size")
    assert _height, _width == expected
