import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_windows(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.os_name", "nt")
    mocker.patch("subprocess.Popen")


@pytest.fixture
def mock_posix(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.os_name", "posix")
    mocker.patch("subprocess.Popen")
