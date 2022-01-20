import os

from Mainframe3270.py3270 import Emulator

from pytest_mock import mocker


CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_emulator_default_args(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "nt")
    mocker.patch("subprocess.Popen")
    under_test = Emulator()

    assert under_test.app.executable == "ws3270"
    assert under_test.app.args == ["-xrm", "ws3270.unlockDelay: False"]


def test_emulator_visible(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "nt")
    mocker.patch("subprocess.Popen")
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "wc3270"
    assert under_test.app.args == [
        "-xrm",
        "wc3270.unlockDelay: False",
        "-xrm",
        "wc3270.model: 2",
    ]


def test_emulator_none_windows(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "posix")
    mocker.patch("subprocess.Popen")
    under_test = Emulator()

    assert under_test.app.executable == "s3270"


def test_emulator_none_windows_visible(mocker):
    mocker.patch("Mainframe3270.py3270.os_name", "posix")
    mocker.patch("subprocess.Popen")
    under_test = Emulator(visible=True)

    assert under_test.app.executable == "x3270"


def test_emulator_with_argfile_oneline():
    argfile = os.path.join(CURDIR, "resources/argfile_oneline.txt")
    under_test = Emulator(argfile=argfile)

    args_from_file = ["--charset", "german"]

    assert all(arg in under_test.app.args for arg in args_from_file)
    assert under_test.app.args > args_from_file


def test_emulator_with_argfile_multiline():
    argfile = os.path.join(CURDIR, "resources/argfile_multiline.txt")
    under_test = Emulator(argfile=argfile)

    args_from_file = ["--charset", "bracket", "--accepthostname", "myhost.com"]

    assert all(arg in under_test.app.args for arg in args_from_file)
    assert under_test.app.args > args_from_file
