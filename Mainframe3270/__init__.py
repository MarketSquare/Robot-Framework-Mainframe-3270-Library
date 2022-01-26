from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robotlibcore import DynamicCore

from .version import VERSION
from .x3270 import x3270


class Mainframe3270(DynamicCore):
    r"""
    Mainframe3270 is a library for Robot Framework based on [https://pypi.org/project/py3270/|py3270 project],
    a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

    = Installation  =

    For use this library you need to install the [http://x3270.bgp.nu/download.html|x3270 project]
    and put the directory on your PATH. On Windows, you need to download wc3270 and put
    the "C:\Program Files\wc3270" in PATH of the Environment Variables.

    = Notes  =

    By default the import set the visible argument to true, on this option the py3270 is running the wc3270.exe,
    but is you set the visible to false, the py3270 will run the ws3270.exe.

    = Example =

    | *** Settings ***
    | Library           Mainframe3270
    | Library           BuiltIn
    |
    | *** Test Cases ***
    | Example
    |     Open Connection    Hostname    LUname
    |     Change Wait Time    0.4
    |     Change Wait Time After Write    0.4
    |     Set Screenshot Folder    C:\\Temp\\IMG
    |     ${value}    Read    3    10    17
    |     Page Should Contain String    ENTER APPLICATION
    |     Wait Field Detected
    |     Write Bare    applicationname
    |     Send Enter
    |     Take Screenshot
    |     Close Connection
    """

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(
        self,
        visible=True,
        timeout="30",
        wait_time="0.5",
        wait_time_after_write="0",
        img_folder=".",
        run_on_failure_keyword="Take Screenshot",
    ):
        """
        You can change to hide the emulator screen set the argument visible=${False}

        For change the wait_time see `Change Wait Time`, to change the img_folder
        see the `Set Screenshot Folder` and to change the timeout see the `Change Timeout` keyword.

        By default, Mainframe3270 will take a screenshot on failure. You can overwrite this to run any other
        keyword by setting the ``run_on_failure_keyword`` option. If you pass ``None`` to this argument, no keyword will be run.
        """
        self._running_on_failure_keyword = False
        self.register_run_on_failure_keyword(run_on_failure_keyword)
        libraries = [
            x3270(visible, timeout, wait_time, wait_time_after_write, img_folder)
        ]
        DynamicCore.__init__(self, libraries)

    @keyword
    def register_run_on_failure_keyword(self, keyword):
        """
        This keyword lets you change the keyword that runs on failure during test execution.
        The default is `Take Screenshot`, which is set on library import.

        You can set ``None`` to this keyword, if you do not want to run any keyword on failure.
        """
        if keyword.lower() == "none":
            self.run_on_failure_keyword = None
        else:
            self.run_on_failure_keyword = keyword

    def run_keyword(self, name, args, kwargs=None):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.run_on_failure()
            raise

    def run_on_failure(self):
        if self._running_on_failure_keyword or not self.run_on_failure_keyword:
            return
        try:
            self._running_on_failure_keyword = True
            BuiltIn().run_keyword(self.run_on_failure_keyword)
        except Exception as error:
            logger.warn(
                f"Keyword '{self.run_on_failure_keyword}' could not be run on failure: {error}"
            )
        finally:
            self._running_on_failure_keyword = False
