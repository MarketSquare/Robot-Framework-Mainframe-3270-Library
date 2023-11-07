import pytest
from pytest_mock import MockerFixture
from robot.api import logger

from Mainframe3270.keywords.read_write import ReadWriteKeywords, SearchResultMode
from Mainframe3270.py3270 import Emulator

from .utils import create_test_object_for


@pytest.fixture
def under_test():
    return create_test_object_for(ReadWriteKeywords)


def test_read(under_test: ReadWriteKeywords, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.string_get", return_value="abc")

    string = under_test.read(1, 1, 3)

    Emulator.string_get.assert_called_once_with(1, 1, 3)
    assert string == "abc"


def test_read_all_screen(under_test: ReadWriteKeywords, mocker: MockerFixture):
    mocker.patch("Mainframe3270.py3270.Emulator.read_all_screen", return_value="all screen")

    content = under_test.read_all_screen()

    Emulator.read_all_screen.assert_called_once()
    assert content == "all screen"


def test_write(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write("abc")

    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_called_once()


def test_write_bare(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_bare("abc")

    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_not_called()


def test_write_in_position(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_in_position("abc", 5, 5)

    Emulator.move_to.assert_called_once_with(5, 5)
    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_called_once()


def test_write_bare_in_position(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.exec_command")
    mocker.patch("Mainframe3270.py3270.Emulator.move_to")
    mocker.patch("Mainframe3270.py3270.Emulator.send_enter")

    under_test.write_bare_in_position("abc", 5, 5)

    Emulator.move_to.assert_called_once_with(5, 5)
    Emulator.exec_command.assert_called_once_with(b'String("abc")')
    Emulator.send_enter.assert_not_called()


def test_get_string_positions(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(5, 10)])

    assert under_test.get_string_positions("abc") == [(5, 10)]

    Emulator.get_string_positions.assert_called_once_with("abc", False)


def test_get_string_positions_as_dict(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(5, 10), (6, 11)])

    assert under_test.get_string_positions("abc", SearchResultMode.As_Dict) == [
        {"ypos": 5, "xpos": 10},
        {"ypos": 6, "xpos": 11},
    ]

    Emulator.get_string_positions.assert_called_once_with("abc", False)


def test_get_string_positions_invalid_mode(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(5, 10)])
    mocker.patch("robot.api.logger.warn")

    assert under_test.get_string_positions("abc", "this is wrong") == [(5, 10)]

    logger.warn.assert_called_with('"mode" should be either "as dict" or "as tuple". Returning the result as tuple')
    Emulator.get_string_positions.assert_called_once_with("abc", False)


def test_get_string_positions_ignore_case(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(5, 10)])

    assert under_test.get_string_positions("abc", ignore_case=True) == [(5, 10)]

    Emulator.get_string_positions.assert_called_once_with("abc", True)


def test_get_string_positions_only_after(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(1, 1), (5, 7)])
    mocker.patch("Mainframe3270.keywords.ReadWriteKeywords._prepare_result_positions")

    under_test.get_string_positions_only_after(5, 6, "my string")

    Emulator.check_limits.assert_called_with(5, 6)
    Emulator.get_string_positions.assert_called_with("my string", False)
    ReadWriteKeywords._prepare_result_positions.assert_called_with(SearchResultMode.As_Tuple, [(5, 7)])


def test_get_string_positions_only_after_as_dict(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(1, 1), (5, 7)])
    mocker.patch("Mainframe3270.keywords.ReadWriteKeywords._prepare_result_positions")

    under_test.get_string_positions_only_after(5, 6, "my string", SearchResultMode.As_Dict)

    Emulator.check_limits.assert_called_with(5, 6)
    Emulator.get_string_positions.assert_called_with("my string", False)
    ReadWriteKeywords._prepare_result_positions.assert_called_with(SearchResultMode.As_Dict, [(5, 7)])


def test_get_string_positions_only_after_ignore_case(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(1, 1), (5, 7)])
    mocker.patch("Mainframe3270.keywords.ReadWriteKeywords._prepare_result_positions")

    under_test.get_string_positions_only_after(5, 6, "my string", ignore_case=True)

    Emulator.check_limits.assert_called_with(5, 6)
    Emulator.get_string_positions.assert_called_with("my string", True)
    ReadWriteKeywords._prepare_result_positions.assert_called_with(SearchResultMode.As_Tuple, [(5, 7)])


def test_get_string_positions_only_before(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(1, 1), (5, 7)])
    mocker.patch("Mainframe3270.keywords.ReadWriteKeywords._prepare_result_positions")

    under_test.get_string_positions_only_before(5, 7, "my string")

    Emulator.check_limits.assert_called_with(5, 7)
    Emulator.get_string_positions.assert_called_with("my string", False)
    ReadWriteKeywords._prepare_result_positions.assert_called_with(SearchResultMode.As_Tuple, [(1, 1)])


def test_get_string_positions_only_before_as_dict(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(1, 1), (5, 7)])
    mocker.patch("Mainframe3270.keywords.ReadWriteKeywords._prepare_result_positions")

    under_test.get_string_positions_only_before(5, 7, "my string", SearchResultMode.As_Dict)

    Emulator.check_limits.assert_called_with(5, 7)
    Emulator.get_string_positions.assert_called_with("my string", False)
    ReadWriteKeywords._prepare_result_positions.assert_called_with(SearchResultMode.As_Dict, [(1, 1)])


def test_get_string_positions_only_before_ignore_case(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("Mainframe3270.py3270.Emulator.check_limits")
    mocker.patch("Mainframe3270.py3270.Emulator.get_string_positions", return_value=[(1, 1), (5, 7)])
    mocker.patch("Mainframe3270.keywords.ReadWriteKeywords._prepare_result_positions")

    under_test.get_string_positions_only_before(5, 7, "my string", ignore_case=True)

    Emulator.check_limits.assert_called_with(5, 7)
    Emulator.get_string_positions.assert_called_with("my string", True)
    ReadWriteKeywords._prepare_result_positions.assert_called_with(SearchResultMode.As_Tuple, [(1, 1)])


def test__prepare_result_positions(under_test: ReadWriteKeywords):
    assert under_test._prepare_result_positions(SearchResultMode.As_Tuple, [(5, 5)]) == [(5, 5)]


def test__prepare_result_positions_as_dict(under_test: ReadWriteKeywords):
    assert under_test._prepare_result_positions(SearchResultMode.As_Dict, [(5, 6)]) == [{"ypos": 5, "xpos": 6}]


def test__prepare_result_positions_invalid_mode(mocker: MockerFixture, under_test: ReadWriteKeywords):
    mocker.patch("robot.api.logger.warn")

    assert under_test._prepare_result_positions("abc", [(5, 10)]) == [(5, 10)]

    logger.warn.assert_called_with('"mode" should be either "as dict" or "as tuple". Returning the result as tuple')
