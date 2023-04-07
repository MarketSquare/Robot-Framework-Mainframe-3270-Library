import os

from pytest_mock import MockerFixture

from Mainframe3270.x3270 import X3270

from .conftest import X3270_DEFAULT_ARGS


def test_default_args():
    under_test = X3270(True, 30, 0.5, 0.0, ".")
    assert under_test.visible is True
    assert under_test.timeout == 30
    assert under_test.wait == 0.5
    assert under_test.wait_write == 0.0
    assert under_test.imgfolder == "."
    under_test.mf is None


def test_import_with_time_string():
    under_test = X3270(True, "30 s", "500 milliseconds", "1 minute", ".")
    assert under_test.timeout == 30
    assert under_test.wait == 0.5
    assert under_test.wait_write == 60


def test_output_folder_robotframework_running(mocker: MockerFixture):
    m_get_variable_value = mocker.patch(
        "robot.libraries.BuiltIn.BuiltIn.get_variable_value",
        return_value="/home/output",
    )
    under_test = X3270(**X3270_DEFAULT_ARGS)

    m_get_variable_value.assert_called_with("${OUTPUT DIR}")
    assert under_test.output_folder == "/home/output"


def test_output_folder_robotframework_not_running(under_test: X3270):
    assert under_test.output_folder == os.getcwd()
