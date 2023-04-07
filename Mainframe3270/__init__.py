from datetime import timedelta
from typing import Any

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robotlibcore import DynamicCore

from .version import VERSION
from .x3270 import X3270


class Mainframe3270(DynamicCore):
    r"""
    Mainframe3270 is a library for Robot Framework based on the [https://pypi.org/project/py3270/|py3270 project],
    a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

    = Installation  =

    For use this library you need to install the [http://x3270.bgp.nu/download.html|x3270 project]
    and put the directory on your PATH. On Windows, you need to download wc3270 and put
    the "C:\Program Files\wc3270" in PATH of the Environment Variables.

    = Example =

    | *** Settings ***
    | Library           Mainframe3270
    |
    | *** Test Cases ***
    | Example
    |     Open Connection    Hostname    LUname
    |     Change Wait Time    0.4 seconds
    |     Change Wait Time After Write    0.4 seconds
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
        visible: bool = True,
        timeout: timedelta = timedelta(seconds=30),
        wait_time: timedelta = timedelta(milliseconds=500),
        wait_time_after_write: timedelta = timedelta(seconds=0),
        img_folder: str = ".",
        run_on_failure_keyword: str = "Take Screenshot",
    ) -> None:
        """
        By default the emulator visibility is set to visible=True.
        In this case test cases are executed using wc3270 (Windows) or x3270 (Linux/MacOSX).
        You can change this by setting visible=False.
        Then test cases are run using ws3720 (Windows) or s3270 (Linux/MacOS).
        This is useful when test cases are run in a CI/CD-pipeline and there is no need for a graphical user interface.

        Timeout, waits and screenshot folder are set on library import as shown above.
        However, they can be changed during runtime. To modify the ``wait_time``, see `Change Wait Time`,
        to modify the ``img_folder``, see `Set Screenshot Folder`,
        and to modify the ``timeout``, see the `Change Timeout` keyword. Timeouts support all available
        Robot Framework [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#time-format|time formats].

        By default, Mainframe3270 will take a screenshot on failure.
        You can overwrite this to run any other keyword by setting the ``run_on_failure_keyword`` option.
        If you pass ``None`` to this argument, no keyword will be run.
        To change the ``run_on_failure_keyword`` during runtime, see `Register Run On Failure Keyword`.
        """
        self._running_on_failure_keyword = False
        self.register_run_on_failure_keyword(run_on_failure_keyword)
        libraries = [
            X3270(visible, timeout, wait_time, wait_time_after_write, img_folder)
        ]
        DynamicCore.__init__(self, libraries)

    @keyword
    def register_run_on_failure_keyword(self, keyword: str) -> None:
        """
        This keyword lets you change the keyword that runs on failure during test execution.
        The default is `Take Screenshot`, which is set on library import.

        You can set ``None`` to this keyword, if you do not want to run any keyword on failure.

        Example:
            | Register Run On Failure Keyword | None | # no keyword is run on failure |
            | Register Run On Failure Keyword | Custom Keyword | # Custom Keyword is run on failure |
        """
        if keyword.lower() == "none":
            self.run_on_failure_keyword = None
        else:
            self.run_on_failure_keyword = keyword

    def run_keyword(self, name: str, args: list, kwargs: dict) -> Any:
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.run_on_failure()
            raise

    def run_on_failure(self) -> None:
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
