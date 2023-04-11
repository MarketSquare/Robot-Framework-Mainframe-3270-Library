import os

from pytest_mock import MockerFixture
from robot.api import logger

from Mainframe3270.x3270 import X3270


def test_set_screenshot_folder(under_test: X3270):
    path = os.getcwd()

    under_test.set_screenshot_folder(path)

    assert under_test.imgfolder == os.getcwd()


def test_set_screenshot_folder_nonexistent(mocker: MockerFixture, under_test: X3270):
    mocker.patch("robot.api.logger.error")
    mocker.patch("robot.api.logger.warn")
    path = os.path.join(os.getcwd(), "nonexistent")

    under_test.set_screenshot_folder(path)

    logger.error.assert_called_with('Given screenshots path "%s" does not exist' % path)
    logger.warn.assert_called_with(
        'Screenshots will be saved in "%s"' % under_test.imgfolder
    )


def test_take_screenshot(mocker: MockerFixture, under_test: X3270):
    mocker.patch("Mainframe3270.py3270.Emulator.save_screen")
    mocker.patch("robot.api.logger.write")
    mocker.patch("time.time", return_value=1.0)

    filepath = under_test.take_screenshot(500, 500)

    logger.write.assert_called_with(
        '<iframe src="./screenshot_1000.html" height="500" width="500"></iframe>',
        level="INFO",
        html=True,
    )
    if os.name == "nt":
        assert filepath == r".\screenshot_1000.html"
    else:
        assert filepath == "./screenshot_1000.html"

    filepath = under_test.take_screenshot(250, 250, "MyScreenshot")

    logger.write.assert_called_with(
        '<iframe src="./MyScreenshot_1000.html" height="250" width="250"></iframe>',
        level="INFO",
        html=True,
    )
    if os.name == "nt":
        assert filepath == r".\MyScreenshot_1000.html"
    else:
        assert filepath == "./MyScreenshot_1000.html"
