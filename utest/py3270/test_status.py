import pytest

from Mainframe3270.py3270 import Status


@pytest.fixture
def under_test():
    status_line = b"U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000"
    return Status(status_line)


def test_status_line(under_test: Status):
    assert under_test.as_string == "U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000"
    assert under_test.keyboard == b"U"
    assert under_test.screen_format == b"U"
    assert under_test.field_protection == b"U"
    assert under_test.connection_state == b"C(pub400.com)"
    assert under_test.emulator_mode == b"C"
    assert under_test.model_number == b"4"
    assert under_test.row_number == b"43"
    assert under_test.col_number == b"80"
    assert under_test.cursor_row == b"4"
    assert under_test.cursor_col == b"24"
    assert under_test.window_id == b"0x0"
    assert under_test.exec_time == b"0.000"


def test__str__(under_test: Status):
    assert str(under_test) == "STATUS: U U U C(pub400.com) C 4 43 80 4 24 0x0 0.000"
