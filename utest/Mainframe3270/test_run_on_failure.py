import pytest
from pytest_mock import MockerFixture
from robot.api import logger

from Mainframe3270 import Mainframe3270


def test_register_run_on_failure_keyword():
    under_test = Mainframe3270()

    under_test.register_run_on_failure_keyword("My Keyword")

    assert under_test.run_on_failure_keyword == "My Keyword"


def test_register_none_to_run_on_failure():
    under_test = Mainframe3270()

    under_test.register_run_on_failure_keyword("None")

    assert under_test.run_on_failure_keyword is None


def test_run_on_failure_could_not_be_run(mocker: MockerFixture):
    mocker.patch(
        "robotlibcore.DynamicCore.run_keyword",
        side_effect=Exception("my error message"),
    )
    mocker.patch(
        "robot.libraries.BuiltIn.BuiltIn.run_keyword",
        side_effect=Exception("my error message"),
    )
    mocker.patch("robot.api.logger.warn")

    under_test = Mainframe3270()

    with pytest.raises(Exception, match="my error message"):
        under_test.run_keyword("Keyword", None, None)
        logger.warn.assert_called_with(
            "Keyword 'Keyword' could not be run on failure: my error message"
        )
