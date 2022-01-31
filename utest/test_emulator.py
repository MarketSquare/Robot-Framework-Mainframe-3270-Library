import os

import pytest

from Mainframe3270.py3270 import Emulator

CURDIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def mock_windows(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "nt")


@pytest.fixture
def mock_posix(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "posix")
    mocker.patch("subprocess.Popen")


def test_emulator_default_args(mock_windows):
    under_test = Emulator()

    assert under_test.app.executable == "ws3270"
    assert under_test.app.args == ["-xrm", "ws3270.unlockDelay: False"]


def test_emulator_visible(mock_windows):
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "wc3270"
    assert under_test.app.args == [
        "-xrm",
        "wc3270.unlockDelay: False",
        "-xrm",
        "wc3270.model: 2",
    ]


def test_emulator_none_windows(mock_posix):
    under_test = Emulator()

    assert under_test.app.executable == "s3270"


def test_emulator_none_windows_visible(mock_posix):
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "x3270"


def test_emulator_with_extra_args_oneline(mock_windows):
    extra_args = os.path.join(CURDIR, "resources/argfile_oneline.txt")
    under_test = Emulator(extra_args=extra_args)

    args_from_file = ["--charset", "german"]

    assert all(arg in under_test.app.args for arg in args_from_file)
    assert under_test.app.args > args_from_file


def test_emulator_none_windows_extra_args_oneline(mock_posix):
    extra_args = os.path.join(CURDIR, "resources/argfile_oneline.txt")
    under_test = Emulator(extra_args=extra_args)

    args_from_file = ["--charset", "german"]

    assert all(arg in under_test.app.args for arg in args_from_file)
    assert under_test.app.args > args_from_file


def test_emulator_with_extra_args_multiline(mock_windows):
    extra_args = os.path.join(CURDIR, "resources/argfile_multiline.txt")
    under_test = Emulator(extra_args=extra_args)

    args_from_file = ["--charset", "bracket", "--accepthostname", "myhost.com"]

    assert all(arg in under_test.app.args for arg in args_from_file)
    assert under_test.app.args > args_from_file


def test_emulator_with_extra_args_multiline_comments(mock_windows):
    extra_args = os.path.join(CURDIR, "resources/argfile_multiline_comments.txt")
    under_test = Emulator(extra_args=extra_args)

    args_from_file = ["--charset", "bracket", "--accepthostname", "myhost.com"]

    assert all(arg in under_test.app.args for arg in args_from_file)
    assert "comment" not in under_test.app.args


def test_emulator_with_extra_args(mock_windows):
    extra_args = ["--cadir", "/path/to/ca_dir"]
    under_test = Emulator(extra_args=extra_args)

    assert all(arg in under_test.app.args for arg in extra_args)
    assert under_test.app.args > extra_args
