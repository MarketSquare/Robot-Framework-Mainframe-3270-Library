import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_subprocess(mocker: MockerFixture):
    mocker.patch("subprocess.Popen")
