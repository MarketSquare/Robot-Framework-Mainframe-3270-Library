import os
from datetime import timedelta
from typing import Any
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import ConnectionCache
from robotlibcore import DynamicCore
from Mainframe3270.keywords import (
    AssertionKeywords,
    CommandKeywords,
    ConnectionKeywords,
    ReadWriteKeywords,
    ScreenshotKeywords,
    WaitAndTimeoutKeywords,
)
from Mainframe3270.py3270 import Emulator
from Mainframe3270.utils import convert_timeout
from Mainframe3270.version import VERSION


class Mainframe3270(DynamicCore):
    r"""
    Mainframe3270 is a library for Robot Framework based on the [https://pypi.org/project/py3270/|py3270 project],
    a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

    = Installation  =

    To use this library, you must have the [http://x3270.bgp.nu/download.html|x3270 project] installed and included in your PATH.
    On Windows, you can install wc3270 and add "C:\Program Files\wc3270" to your PATH in the Environment Variables.

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

    = Concurrent Connections =

    The library allows you to have multiple sessions open at the same time. Each session opened by `Open Connection` or
    `Open Connection From Session File` will return an index that can be used to reference it
    when switching between connections using the `Switch Connection` keyword. The indices start from 1 and are incremented
    by each newly opened connection. Calling `Close All Connection` will reset the index counter to 1.

    Additionally, you can provide aliases to your sessions when opening a connection, and switch the connection
    using that alias instead of the index.

    It is worth noting that the connection that was opened last is always the current connection.

    | *** Test Cases ***
    | Concurrent Sessions
    |     ${index_1}    Open Connection    Hostname    # this is the current connection
    |     Write Bare    First String
    |     ${index_2}    Open Connection    Hostname    alias=second    # 'second' is now the current connection
    |     Write Bare    Second String
    |     Switch Connection    ${index_1}    # swtiching the connection using the index
    |     Page Should Contain String    First String
    |     Switch Connection    second    # switchting the ocnnection using the alias
    |     Page Should Contain String    Second String
    |     [Teardown]    Close All Connections

    = Changing the emulator model (experimental) =

    By default, the library uses the emulator model 2, which is 24 rows by 80 columns.
    You can, however, change the model globally when `importing` the library with the `model` argument
    set to the model of your choice.

    The basic models are 2, 3, 4, and 5. These models differ in their screen size as illustrated in this table:

    | *3270 Model* | *Rows* | *Columns* |
    | 2            | 24     | 80        |
    | 3            | 32     | 80        |
    | 4            | 43     | 80        |
    | 5            | 27     | 132       |


    They can be combined with the 3278 (monochrome green-screen) or 3279 (color) prefix, e.g. 3278-2 or 3279-2.

    In addition to that, there is a -E suffix that indicates support for the [https://x3270.miraheze.org/wiki/3270_data_stream_protocol#extended|x3270 extended data stream].

    You can find more information on emulator models on the [https://x3270.miraheze.org/wiki/3270_models|x3270 wiki].

    In addition to setting the model globally, you can also set the model on the individual emulator basis by providing the model arguments to the `Open Connection`
    or `Open Connection From Session File` keywords.

    Here is an example for setting the emulator in the Open Connection keyword:

    | Open Connection    pub400.com    extra_args=["-xrm", "*model: 4"]

    And this is how you would set the emulator model in the Open Connection From Session File keyword:

    | Open Connection From Session File    /path/to/session/file

    Where the content of the session file would be

    | *hostname: pub400.com
    | *model: 4


    Note that this is an experimental feature, so not all models might work as expected.
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
        model: str = "2",
    ) -> None:
        """
        By default, the emulator visibility is set to visible=True.
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
        self.visible = visible
        self.timeout = convert_timeout(timeout)
        self.wait_time = convert_timeout(wait_time)
        self.wait_time_after_write = convert_timeout(wait_time_after_write)
        self.img_folder = img_folder
        self._running_on_failure_keyword = False
        self.register_run_on_failure_keyword(run_on_failure_keyword)
        self.model = model
        self.cache = ConnectionCache()
        # When generating the library documentation with libdoc, BuiltIn.get_variable_value throws
        # a RobotNotRunningError. Therefore, we catch it here to be able to generate the documentation.
        try:
            self.output_folder = BuiltIn().get_variable_value("${OUTPUT DIR}")
        except RobotNotRunningError:
            self.output_folder = os.getcwd()
        libraries = [
            AssertionKeywords(self),
            CommandKeywords(self),
            ConnectionKeywords(self),
            ReadWriteKeywords(self),
            ScreenshotKeywords(self),
            WaitAndTimeoutKeywords(self),
        ]
        DynamicCore.__init__(self, libraries)

    @property
    def mf(self) -> Emulator:
        return self.cache.current

    @keyword("Register Run On Failure Keyword")
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
            logger.warn(f"Keyword '{self.run_on_failure_keyword}' could not be run on failure: {error}")
        finally:
            self._running_on_failure_keyword = False
