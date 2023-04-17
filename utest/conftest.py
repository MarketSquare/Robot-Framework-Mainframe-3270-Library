import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_subprocess(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")


@pytest.fixture
def mock_windows(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.os_name", "nt")
    mocker.patch("Mainframe3270.x3270.os_name", "nt")


@pytest.fixture
def mock_posix(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.os_name", "posix")
    mocker.patch("Mainframe3270.x3270.os_name", "posix")
