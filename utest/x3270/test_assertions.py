import re

import pytest
from pytest_mock import MockerFixture
from robot.api import logger

from Mainframe3270.py3270 import Emulator


def test_page_should_contain_string(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")
    mocker.patch("robot.api.logger.info")

    Emulator().page_should_contain_string("abc")

    logger.info.assert_called_with('The string "abc" was found')


def test_page_should_contain_string_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="aBc")
    mocker.patch("robot.api.logger.info")

    Emulator().page_should_contain_string("abc", ignore_case=True)

    logger.info.assert_called_with('The string "abc" was found')


def test_page_should_contain_string_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='The string "def" was not found'):
        Emulator().page_should_contain_string("def")


def test_page_should_contain_string_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_contain_string("def", error_message="my error message")


def test_page_should_not_contain_string(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_not_contain_string("ABC")


def test_page_should_not_contain_string_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_not_contain_string("def", ignore_case=True)


def test_page_should_not_contain_string_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='The string "ABC" was found'):
        Emulator().page_should_not_contain_string("ABC", ignore_case=True)


def test_page_should_not_contain_string_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_not_contain_string(
            "abc", error_message="my error message"
        )


def test_page_should_contain_any_string(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_contain_any_string(["abc", "def"])


def test_page_should_contain_any_string_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_contain_any_string(["ABC", "def"], ignore_case=True)


def test_page_should_contain_any_string_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(
        Exception, match=re.escape("The strings \"['def', 'ghi']\" were not found")
    ):
        Emulator().page_should_contain_any_string(["def", "ghi"])


def test_page_should_contain_any_string_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_contain_any_string(
            ["def", "ghi"], error_message="my error message"
        )


def test_page_should_contain_all_strings(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", side_effect=["abc", "def"])

    Emulator().page_should_contain_all_strings(["abc", "def"])


def test_page_should_contain_all_strings_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", side_effect=["AbC", "DeF"])

    Emulator().page_should_contain_all_strings(["abc", "def"], ignore_case=True)


def test_page_should_contain_all_strings_fails(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value=["def"])

    with pytest.raises(Exception, match='The string "ghi" was not found'):
        Emulator().page_should_contain_all_strings(["def", "ghi"])


def test_page_should_contain_all_strings_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_contain_all_strings(
            ["abc", "def"], error_message="my error message"
        )


def test_page_should_not_contain_any_string(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_not_contain_any_string(["def", "ghi"])


def test_page_should_not_contain_any_string_fails(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='The string "abc" was found'):
        Emulator().page_should_not_contain_any_string(["abc", "def"])


def test_page_should_not_contain_any_string_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="ABC")

    with pytest.raises(Exception, match='The string "abc" was found'):
        Emulator().page_should_not_contain_any_string(["abc", "def"], ignore_case=True)


def test_page_should_not_contain_any_string_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_not_contain_any_string(
            ["abc", "def"], error_message="my error message"
        )


def test_page_should_not_contain_all_strings(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_not_contain_all_strings(["def", "ghi"])


def test_page_should_not_contain_all_strings_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='The string "abc" was found'):
        Emulator().page_should_not_contain_all_strings(["ABC", "def"], ignore_case=True)


def test_page_should_not_contain_all_strings_fails(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match='The string "abc" was found'):
        Emulator().page_should_not_contain_all_strings(["abc", "def"])


def test_page_should_not_contain_all_strings_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_not_contain_all_strings(
            ["abc", "def"], error_message="my error message"
        )


def test_page_should_contain_string_x_times(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")

    Emulator().page_should_contain_string_x_times("a", 24)


def test_page_should_contain_string_x_times_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")

    Emulator().page_should_contain_string_x_times("A", 24, ignore_case=True)


def test_page_should_contain_string_x_times_fails(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")

    with pytest.raises(
        Exception, match='The string "a" was not found "1" times, it appears "24" times'
    ):
        Emulator().page_should_contain_string_x_times("a", 1)

    with pytest.raises(
        Exception, match='The string "b" was not found "1" times, it appears "0" times'
    ):
        Emulator().page_should_contain_string_x_times("b", 1)


def test_page_should_contain_string_x_times_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_contain_string_x_times(
            "b", 1, error_message="my error message"
        )


def test_page_should_match_regex(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_match_regex(r"\w+")


def test_page_should_match_regex_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(
        Exception, match=re.escape(r'No matches found for "\d+" pattern')
    ):
        Emulator().page_should_match_regex(r"\d+")


def test_page_should_not_match_regex(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_not_match_regex(r"\d+")


def test_page_should_not_match_regex_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="a")

    with pytest.raises(
        Exception, match=re.escape('There are matches found for "[a]+" pattern')
    ):
        Emulator().page_should_not_match_regex("[a]+")


def test_page_should_contain_match(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_contain_match("*a?c*")


def test_page_should_contain_match_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(
        Exception, match=re.escape('No matches found for "*e?g*" pattern')
    ):
        Emulator().page_should_contain_match("*e?g*")


def test_page_should_contain_match_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="ABC")

    Emulator().page_should_contain_match("*a?c*", ignore_case=True)


def test_page_should_contain_match_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_contain_match("*def*", error_message="my error message")


def test_page_should_not_contain_match(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    Emulator().page_should_not_contain_match("*def*")


def test_page_should_not_contain_match_fails(mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(
        Exception, match=re.escape('There are matches found for "*abc*" pattern')
    ):
        Emulator().page_should_not_contain_match("*abc*")


def test_page_should_not_contain_match_ignore_case(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(
        Exception, match=re.escape('There are matches found for "*abc*" pattern')
    ):
        Emulator().page_should_not_contain_match("*ABC*", ignore_case=True)


def test_page_should_not_contain_match_custom_message(
    mocker: MockerFixture
):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    with pytest.raises(Exception, match="my error message"):
        Emulator().page_should_not_contain_match(
            "*abc*", error_message="my error message"
        )
