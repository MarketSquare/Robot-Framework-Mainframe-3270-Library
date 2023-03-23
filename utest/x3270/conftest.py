import pytest
from pytest_mock import MockerFixture

from Mainframe3270.py3270 import Emulator
from Mainframe3270.x3270 import X3270

X3270_DEFAULT_ARGS = {
    "visible": True,
    "timeout": 30,
    "wait_time": 0.5,
    "wait_time_after_write": 0.0,
    "img_folder": ".",
}


@pytest.fixture
def under_test(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.create_app")
    under_test = X3270(**X3270_DEFAULT_ARGS)
    under_test.mf = Emulator(under_test.visible, under_test.timeout)
    return under_test
