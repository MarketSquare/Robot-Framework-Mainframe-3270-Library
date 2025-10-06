import os
from pytest_mock import MockerFixture
from Mainframe3270 import Mainframe3270


def test_default_args():
    under_test = Mainframe3270()
    assert under_test.visible is True
    assert under_test.timeout == 30
    assert under_test.wait_time == 0.5
    assert under_test.wait_time_after_write == 0.0
    assert under_test.img_folder == "."
    assert under_test.model == "2"
    under_test.mf is None


def test_import_with_time_string():
    under_test = Mainframe3270(True, "30 s", "500 milliseconds", "1 minute", ".")
    assert under_test.timeout == 30
    assert under_test.wait_time == 0.5
    assert under_test.wait_time_after_write == 60


def test_output_folder_robotframework_running(mocker: MockerFixture):
    m_get_variable_value = mocker.patch(
        "robot.libraries.BuiltIn.BuiltIn.get_variable_value",
        return_value="/home/output",
    )
    under_test = Mainframe3270()

    m_get_variable_value.assert_called_with("${OUTPUT DIR}")
    assert under_test.output_folder == "/home/output"


def test_output_folder_robotframework_not_running():
    under_test = Mainframe3270()

    assert under_test.output_folder == os.getcwd()
