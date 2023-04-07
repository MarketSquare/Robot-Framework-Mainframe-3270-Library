import os
import re
import shlex
import socket
import time
from datetime import timedelta
from os import name as os_name
from typing import Any, List, Optional, Union

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import Matcher, secs_to_timestr, timestr_to_secs

from .py3270 import Emulator


class X3270(object):
    def __init__(
        self,
        visible: bool,
        timeout: timedelta,
        wait_time: timedelta,
        wait_time_after_write: timedelta,
        img_folder: str,
    ) -> None:
        self.visible = visible
        self.timeout = self._convert_timeout(timeout)
        self.wait = self._convert_timeout(wait_time)
        self.wait_write = self._convert_timeout(wait_time_after_write)
        self.imgfolder = img_folder
        self.mf: Emulator = None  # type: ignore
        # Try Catch to run in Pycharm, and make a documentation in libdoc with no error
        try:
            self.output_folder = BuiltIn().get_variable_value("${OUTPUT DIR}")
        except RobotNotRunningError:
            self.output_folder = os.getcwd()

    def _convert_timeout(self, time):
        if isinstance(time, timedelta):
            return time.total_seconds()
        return timestr_to_secs(time, round_to=None)

    @keyword("Change Timeout")
    def change_timeout(self, seconds: timedelta) -> None:
        """
        Change the timeout for connection in seconds.

        Example:
            | Change Timeout | 3 seconds |
        """
        self.timeout = self._convert_timeout(seconds)

    @keyword("Open Connection")
    def open_connection(
        self,
        host: str,
        LU: Optional[str] = None,
        port: int = 23,
        extra_args: Optional[Union[List[str], os.PathLike]] = None,
    ):
        """Create a connection to an IBM3270 mainframe with the default port 23.
        To establish a connection, only the hostname is required. Optional parameters include logical unit name (LU) and port.

        Additional configuration data can be provided through the `extra_args` parameter.
        `extra_args` accepts either a list or a path to a file containing [https://x3270.miraheze.org/wiki/Category:Command-line_options|x3270 command line options].

        Entries in the argfile can be on one line or multiple lines. Lines starting with "#" are considered comments.
        Arguments containing whitespace must be enclosed in single or double quotes.

        | # example_argfile_oneline.txt
        | -accepthostname myhost.com

        | # example_argfile_multiline.txt
        | -xrm "wc3270.acceptHostname: myhost.com"
        | # this is a comment
        | -charset french
        | -port 992

        Please ensure that the arguments provided are available for your specific x3270 application and version.
        Refer to the [https://x3270.miraheze.org/wiki/Wc3270/Command-line_options|wc3270 command line options] for a subset of available options.

        Note: If you specify the port with the `-port` command-line option in `extra_args` (or use the -xrm resource command for it),
        it will take precedence over the `port` argument provided in the `Open Connection` keyword.

        Example:
            | Open Connection | Hostname |
            | Open Connection | Hostname | LU=LUname |
            | Open Connection | Hostname | port=992 |
            | @{extra_args}   | Create List | -accepthostname | myhost.com | -cafile | ${CURDIR}/cafile.crt |
            | Append To List  | ${extra_args} | -port | 992 |
            | Open Connection | Hostname | extra_args=${extra_args} |
            | Open Connection | Hostname | extra_args=${CURDIR}/argfile.txt |
        """
        if self.mf:
            self.close_connection()
        extra_args = self._process_args(extra_args)
        self.mf = Emulator(self.visible, self.timeout, extra_args)
        host_string = f"{LU}@{host}" if LU else host
        if self._port_in_extra_args(extra_args):
            if port != 23:
                logger.warn(
                    "The connection port has been specified both in the `port` argument and in `extra_args`. "
                    "The port specified in `extra_args` will take precedence over the `port` argument. "
                    "To avoid this warning, you can either remove the port command-line option from `extra_args`, "
                    "or leave the `port` argument at its default value of 23."
                )
            self.mf.connect(host_string)
        else:
            self.mf.connect(f"{host_string}:{port}")

    def _process_args(self, args) -> list:
        processed_args = []
        if not args:
            return []
        elif isinstance(args, list):
            processed_args = args
        elif isinstance(args, os.PathLike) or isinstance(args, str):
            with open(args) as file:
                for line in file:
                    if line.lstrip().startswith("#"):
                        continue
                    for arg in shlex.split(line):
                        processed_args.append(arg)
        return processed_args

    def _port_in_extra_args(self, args) -> bool:
        if not args:
            return False
        for arg in args:
            if arg == "-port" or ".port" in arg:
                return True
        return False

    @keyword("Open Connection From Session File")
    def open_connection_from_session_file(self, session_file: os.PathLike):
        """Create a connection to an IBM3270 mainframe using a [https://x3270.miraheze.org/wiki/Session_file|session file].

        The session file contains [https://x3270.miraheze.org/wiki/Category:Resources|resources (settings)] for a specific host session.
        The only mandatory setting required to establish the connection is the [https://x3270.miraheze.org/wiki/Hostname_resource|hostname resource].

        This keyword is an alternative to `Open Connection`. Please note that the Robot-Framework-Mainframe-3270-Library
        currently only supports model "2". Specifying any other model will result in a failure.

        For more information on session file syntax and detailed examples, please consult the [https://x3270.miraheze.org/wiki/Session_file|x3270 wiki].

        Example:
        | Open Connection From Session File | ${CURDIR}/session.wc3270 |

        where the content of `session.wc3270` is:
        | wc3270.hostname: myhost.com:23
        | wc3270.model: 2
        """
        if self.mf:
            self.close_connection()
        self._check_session_file_extension(session_file)
        self._check_contains_hostname(session_file)
        self._check_model(session_file)
        if os_name == "nt" and self.visible:
            self.mf = Emulator(self.visible, self.timeout)
            self.mf.connect(str(session_file))
        else:
            self.mf = Emulator(self.visible, self.timeout, [str(session_file)])

    def _check_session_file_extension(self, session_file):
        file_extension = str(session_file).rsplit(".")[-1]
        expected_extensions = {
            ("nt", True): "wc3270",
            ("nt", False): "ws3270",
            ("posix", True): "x3270",
            ("posix", False): "s3270",
        }
        expected_extension = expected_extensions.get((os_name, self.visible))
        if file_extension != expected_extension:
            raise ValueError(
                f"Based on the emulator that you are using, "
                f'the session file extension has to be ".{expected_extension}", '
                f'but it was ".{file_extension}"'
            )

    def _check_contains_hostname(self, session_file):
        with open(session_file) as file:
            if "hostname:" not in file.read():
                raise ValueError(
                    "Your session file needs to specify the hostname resource "
                    "to set up the connection. "
                    "An example for wc3270 looks like this: \n"
                    "wc3270.hostname: myhost.com\n"
                )

    def _check_model(self, session_file):
        with open(session_file) as file:
            pattern = re.compile(r"[wcxs3270.*]+model:\s*([327892345E-]+)")
            match = pattern.findall(file.read())
            if not match:
                return
            elif match[-1] == "2":
                return
            else:
                raise ValueError(
                    f'Robot-Framework-Mainframe-3270-Library currently only supports model "2", '
                    f'the model you specified in your session file was "{match[-1]}". '
                    f'Please change it to "2", using either the session wizard if you are on Windows, '
                    f'or by editing the model resource like this "*model: 2"'
                )

    @keyword("Close Connection")
    def close_connection(self) -> None:
        """Disconnect from the host."""
        try:
            self.mf.terminate()
        except socket.error:
            pass
        self.mf = None  # type: ignore

    @keyword("Change Wait Time")
    def change_wait_time(self, wait_time: timedelta) -> None:
        """To give time for the mainframe screen to be "drawn" and receive the next commands, a "wait time" has been
        created, which by default is set to 0.5 seconds. This is a sleep applied AFTER the following keywords:

        - `Execute Command`
        - `Send Enter`
        - `Send PF`
        - `Write`
        - `Write in position`

        If you want to change this value, just use this keyword passing the time in seconds.

        Example:
            | Change Wait Time | 0.5              |
            | Change Wait Time | 200 milliseconds |
            | Change Wait Time | 0:00:01.500      |
        """
        self.wait = self._convert_timeout(wait_time)

    @keyword("Change Wait Time After Write")
    def change_wait_time_after_write(self, wait_time_after_write: timedelta) -> None:
        """To give the user time to see what is happening inside the mainframe, a "wait time after write" has
        been created, which by default is set to 0 seconds. This is a sleep applied AFTER sending a string in these
        keywords:

        - `Write`
        - `Write Bare`
        - `Write in position`
        - `Write Bare in position`

        If you want to change this value, just use this keyword passing the time in seconds.

        Note: This keyword is useful for debug purpose

        Example:
            | Change Wait Time After Write | 1             |
            | Change Wait Time After Write | 0.5 seconds   |
            | Change Wait Time After Write | 0:00:02       |
        """
        self.wait_write = self._convert_timeout(wait_time_after_write)

    @keyword("Read")
    def read(self, ypos: int, xpos: int, length: int) -> str:
        """Get a string of ``length`` at screen co-ordinates ``ypos`` / ``xpos``.

        Co-ordinates are 1 based, as listed in the status area of the terminal.

        Example for read a string in the position y=8 / x=10 of a length 15:
            | ${value} | Read | 8 | 10 | 15 |
        """
        self._check_limits(ypos, xpos)
        # Checks if the user has passed a length that will be larger than the x limit of the screen.
        if (xpos + length) > (80 + 1):
            raise Exception(
                "You have exceeded the x-axis limit of the mainframe screen"
            )
        string = self.mf.string_get(ypos, xpos, length)
        return string

    @keyword("Read All Screen")
    def read_all_screen(self) -> str:
        """Read the current screen and returns all content in one string.

        This is useful if your automation scripts should take different routes depending
        on a message shown on the screen.

        Example:
            | ${screen} | Read All Screen              |
            | IF   | 'certain text' in '''${screen}''' |
            |      | Do Something                      |
            | ELSE |                                   |
            |      | Do Something Else                 |
            | END  |                                   |
        """
        return self._read_all_screen()

    @keyword("Execute Command")
    def execute_command(self, cmd: str) -> None:
        """Execute a [http://x3270.bgp.nu/wc3270-man.html#Actions|x3270 command].

        Example:
            | Execute Command | Enter |
            | Execute Command | Home |
            | Execute Command | Tab |
            | Execute Command | PF(1) |
        """
        self.mf.exec_command(cmd.encode("utf-8"))
        time.sleep(self.wait)

    @keyword("Set Screenshot Folder")
    def set_screenshot_folder(self, path: str) -> None:
        r"""Set a folder to keep the html files generated by the `Take Screenshot` keyword.

        Note that the folder needs to exist before running your automation scripts. Else the images
        will be stored in the ``${OUTPUT DIR}`` set by robotframework.

        Example:
            | Set Screenshot Folder | C:\\Temp\\Images |
        """
        if os.path.exists(os.path.normpath(os.path.join(self.output_folder, path))):
            self.imgfolder = path
        else:
            logger.error('Given screenshots path "%s" does not exist' % path)
            logger.warn('Screenshots will be saved in "%s"' % self.imgfolder)

    @keyword("Take Screenshot")
    def take_screenshot(
        self, height: int = 410, width: int = 670, filename_prefix: str = "screenshot"
    ) -> str:
        """Generate a screenshot of the IBM 3270 Mainframe in a html format. The
        default folder is the log folder of RobotFramework, if you want change see the `Set Screenshot Folder`.

        The Screenshot is printed in a iframe log, with the values of height=410 and width=670, you
        can change these values by passing them to the keyword.

        The file name prefix can be set, the default is "screenshot".

        The full file path is returned.

        Example:
            | ${filepath} | Take Screenshot |
            | ${filepath} | Take Screenshot | height=500 | width=700 |
            | Take Screenshot | height=500 | width=700 |
            | Take Screenshot | filename_prefix=MyScreenshot |
        """
        extension = "html"
        filename_sufix = round(time.time() * 1000)
        filepath = os.path.join(
            self.imgfolder, "%s_%s.%s" % (filename_prefix, filename_sufix, extension)
        )
        self.mf.save_screen(os.path.join(self.output_folder, filepath))
        logger.write(
            '<iframe src="%s" height="%s" width="%s"></iframe>'
            % (filepath.replace("\\", "/"), height, width),
            level="INFO",
            html=True,
        )
        return filepath

    @keyword("Wait Field Detected")
    def wait_field_detected(self) -> None:
        """Wait until the screen is ready, the cursor has been positioned
        on a modifiable field, and the keyboard is unlocked.

        Sometimes the server will "unlock" the keyboard but the screen
        will not yet be ready.  In that case, an attempt to read or write to the
        screen will result in a 'E' keyboard status because we tried to read from
        a screen that is not ready yet.

        Using this method tells the client to wait until a field is
        detected and the cursor has been positioned on it.
        """
        self.mf.wait_for_field()

    @keyword("Delete Char")
    def delete_char(
        self, ypos: Optional[int] = None, xpos: Optional[int] = None
    ) -> None:
        """Delete the character under the cursor. If you want to delete a character that is in
        another position, simply pass the coordinates ``ypos`` / ``xpos``.

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Delete Char |
            | Delete Char | ypos=9 | xpos=25 |
        """
        if ypos is not None and xpos is not None:
            self.mf.move_to(ypos, xpos)
        self.mf.exec_command(b"Delete")

    @keyword("Delete Field")
    def delete_field(
        self, ypos: Optional[int] = None, xpos: Optional[int] = None
    ) -> None:
        """Delete the entire content of a field at the current cursor location and positions
        the cursor at beginning of field. If you want to delete a field that is in
        another position, simply pass the coordinates ``ypos`` / ``xpos`` of any part in the field.

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Delete Field |
            | Delete Field | ypos=12 | xpos=6 |
        """
        if ypos is not None and xpos is not None:
            self.mf.move_to(ypos, xpos)
        self.mf.delete_field()

    @keyword("Send Enter")
    def send_enter(self) -> None:
        """Send an Enter to the screen."""
        self.mf.send_enter()
        time.sleep(self.wait)

    @keyword("Move Next Field")
    def move_next_field(self) -> None:
        """Move the cursor to the next input field. Equivalent to pressing the Tab key."""
        self.mf.exec_command(b"Tab")

    @keyword("Move Previous Field")
    def move_previous_field(self) -> None:
        """Move the cursor to the previous input field. Equivalent to pressing the Shift+Tab keys."""
        self.mf.exec_command(b"BackTab")

    @keyword("Send PF")
    def send_PF(self, PF: str) -> None:
        """Send a Program Function to the screen.

        Example:
               | Send PF | 3 |
        """
        self.mf.exec_command(("PF({0})").format(PF).encode("utf-8"))
        time.sleep(self.wait)

    @keyword("Write")
    def write(self, txt: str) -> None:
        """Send a string *and Enter* to the screen at the current cursor location.

        Example:
            | Write | something |
        """
        self._write(txt, enter=1)

    @keyword("Write Bare")
    def write_bare(self, txt: str) -> None:
        """Send only the string to the screen at the current cursor location.

        Example:
            | Write Bare | something |
        """
        self._write(txt)

    @keyword("Write In Position")
    def write_in_position(self, txt: str, ypos: int, xpos: int) -> None:
        """Send a string *and Enter* to the screen at screen co-ordinates ``ypos`` / ``xpos``.

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Write in Position | something | 9 | 11 |
        """
        self._write(txt, ypos, xpos, enter=1)

    @keyword("Write Bare In Position")
    def write_bare_in_position(self, txt: str, ypos: int, xpos: int):
        """Send only the string to the screen at screen co-ordinates ``ypos`` / ``xpos``.

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Write Bare in Position | something | 9 | 11 |
        """
        self._write(txt, ypos, xpos)

    def _write(
        self,
        txt: Any,
        ypos: Optional[int] = None,
        xpos: Optional[int] = None,
        enter: int = 0,
    ) -> None:
        txt = txt.encode("unicode_escape")
        if ypos is not None and xpos is not None:
            self._check_limits(ypos, xpos)
            self.mf.send_string(txt, ypos, xpos)
        else:
            self.mf.send_string(txt)
        time.sleep(self.wait_write)
        for i in range(enter):
            self.mf.send_enter()
            time.sleep(self.wait)

    @keyword("Wait Until String")
    def wait_until_string(
        self, txt: str, timeout: timedelta = timedelta(seconds=5)
    ) -> str:
        """Wait until a string exists on the mainframe screen to perform the next step. If the string does not appear in
        5 seconds, the keyword will raise an exception. You can define a different timeout.

        Example:
            | Wait Until String | something |
            | Wait Until String | something | 10 |
            | Wait Until String | something | 15 s |
            | Wait Until String | something | 0:00:15 |
        """
        timeout = self._convert_timeout(timeout)
        max_time = time.time() + timeout  # type: ignore
        while time.time() < max_time:
            result = self._search_string(str(txt))
            if result:
                return txt
        raise Exception(f'String "{txt}" not found in {secs_to_timestr(timeout)}')

    def _search_string(self, string: str, ignore_case: bool = False) -> bool:
        """Search if a string exists on the mainframe screen and return True or False."""

        def __read_screen(string: str, ignore_case: bool) -> bool:
            for ypos in range(24):
                line = self.mf.string_get(ypos + 1, 1, 80)
                if ignore_case:
                    line = line.lower()
                if string in line:
                    return True
            return False

        status = __read_screen(string, ignore_case)
        return status

    @keyword("Page Should Contain String")
    def page_should_contain_string(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that a given string exists on the mainframe screen.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain String | something |
            | Page Should Contain String | someTHING | ignore_case=True                |
            | Page Should Contain String | something | error_message=New error message |
        """
        message = f'The string "{txt}" was not found'
        if error_message:
            message = error_message
        if ignore_case:
            txt = txt.lower()
        result = self._search_string(txt, ignore_case)
        if not result:
            raise Exception(message)
        logger.info(f'The string "{txt}" was found')

    @keyword("Page Should Not Contain String")
    def page_should_not_contain_string(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that a given string does NOT exists on the mainframe screen.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain String | something |
            | Page Should Not Contain String | someTHING | ignore_case=True |
            | Page Should Not Contain String | something | error_message=New error message |
        """
        message = f'The string "{txt}" was found'
        if error_message:
            message = error_message
        if ignore_case:
            txt = txt.lower()
        result = self._search_string(txt, ignore_case)
        if result:
            raise Exception(message)

    @keyword("Page Should Contain Any String")
    def page_should_contain_any_string(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Assert that one of the strings in a given list exists on the mainframe screen.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain Any String | ${list_of_string} |
            | Page Should Contain Any String | ${list_of_string} | ignore_case=True |
            | Page Should Contain Any String | ${list_of_string} | error_message=New error message |
        """
        message = f'The strings "{list_string}" were not found'
        if error_message:
            message = error_message
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self._search_string(string, ignore_case)
            if result:
                break
        if not result:
            raise Exception(message)

    @keyword("Page Should Not Contain Any String")
    def page_should_not_contain_any_string(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Assert that none of the strings in a given list exists on the mainframe screen. If one or more of the
        string are found, the keyword will raise a exception.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain Any Strings | ${list_of_string} |
            | Page Should Not Contain Any Strings | ${list_of_string} | ignore_case=True |
            | Page Should Not Contain Any Strings | ${list_of_string} | error_message=New error message |
        """
        self._compare_all_list_with_screen_text(
            list_string, ignore_case, error_message, should_match=False
        )

    @keyword("Page Should Contain All Strings")
    def page_should_contain_all_strings(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Assert that all of the strings in a given list exist on the mainframe screen.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain All Strings | ${list_of_string} |
            | Page Should Contain All Strings | ${list_of_string} | ignore_case=True |
            | Page Should Contain All Strings | ${list_of_string} | error_message=New error message |
        """
        self._compare_all_list_with_screen_text(
            list_string, ignore_case, error_message, should_match=True
        )

    @keyword("Page Should Not Contain All Strings")
    def page_should_not_contain_all_strings(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Fails if one of the strings in a given list exists on the mainframe screen. If one of the string
        are found, the keyword will raise a exception.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain All Strings | ${list_of_string} |
            | Page Should Not Contain All Strings | ${list_of_string} | ignore_case=True |
            | Page Should Not Contain All Strings | ${list_of_string} | error_message=New error message |
        """
        message = error_message
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self._search_string(string, ignore_case)
            if result:
                if message is None:
                    message = f'The string "{string}" was found'
                raise Exception(message)

    @keyword("Page Should Contain String X Times")
    def page_should_contain_string_x_times(
        self,
        txt: str,
        number: int,
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Asserts that the entered string appears the desired number of times on the mainframe screen.

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
               | Page Should Contain String X Times | something | 3 |
               | Page Should Contain String X Times | someTHING | 3 | ignore_case=True |
               | Page Should Contain String X Times | something | 3 | error_message=New error message |
        """
        message = error_message
        number = number
        all_screen = self._read_all_screen()
        if ignore_case:
            txt = txt.lower()
            all_screen = all_screen.lower()
        number_of_times = all_screen.count(txt)
        if number_of_times != number:
            if message is None:
                message = f'The string "{txt}" was not found "{number}" times, it appears "{number_of_times}" times'
            raise Exception(message)
        logger.info(f'The string "{txt}" was found "{number}" times')

    @keyword("Page Should Match Regex")
    def page_should_match_regex(self, regex_pattern: str) -> None:
        r"""Fails if string does not match pattern as a regular expression. Regular expression check is
        implemented using the Python [https://docs.python.org/2/library/re.html|re module]. Python's
        regular expression syntax is derived from Perl, and it is thus also very similar to the syntax used,
        for example, in Java, Ruby and .NET.

        Backslash is an escape character in the test data, and possible backslashes in the pattern must
        thus be escaped with another backslash (e.g. \\d\\w+).
        """
        page_text = self._read_all_screen()
        if not re.findall(regex_pattern, page_text, re.MULTILINE):
            raise Exception(f'No matches found for "{regex_pattern}" pattern')

    @keyword("Page Should Not Match Regex")
    def page_should_not_match_regex(self, regex_pattern: str) -> None:
        r"""Fails if string does match pattern as a regular expression. Regular expression check is
        implemented using the Python [https://docs.python.org/2/library/re.html|re module]. Python's
        regular expression syntax is derived from Perl, and it is thus also very similar to the syntax used,
        for example, in Java, Ruby and .NET.

        Backslash is an escape character in the test data, and possible backslashes in the pattern must
        thus be escaped with another backslash (e.g. \\d\\w+).
        """
        page_text = self._read_all_screen()
        if re.findall(regex_pattern, page_text, re.MULTILINE):
            raise Exception(f'There are matches found for "{regex_pattern}" pattern')

    @keyword("Page Should Contain Match")
    def page_should_contain_match(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that the text displayed on the mainframe screen matches the given pattern.

        Pattern matching is similar to matching files in a shell, and it is always case sensitive.
        In the pattern, * matches anything and ? matches any single character.

        Note that for this keyword the entire screen is considered a string. So if you want to search
        for the string "something" and it is somewhere other than at the beginning or end of the screen, it
        should be reported as follows: **something**

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain Match | **something** |
            | Page Should Contain Match | **so???hing** |
            | Page Should Contain Match | **someTHING** | ignore_case=True |
            | Page Should Contain Match | **something** | error_message=New error message |
        """
        message = error_message
        all_screen = self._read_all_screen()
        if ignore_case:
            txt = txt.lower()
            all_screen = all_screen.lower()
        matcher = Matcher(txt, caseless=False, spaceless=False)
        result = matcher.match(all_screen)
        if not result:
            if message is None:
                message = f'No matches found for "{txt}" pattern'
            raise Exception(message)

    @keyword("Page Should Not Contain Match")
    def page_should_not_contain_match(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that the text displayed on the mainframe screen does NOT match the given pattern.

        Pattern matching is similar to matching files in a shell, and it is always case sensitive.
        In the pattern, * matches anything and ? matches any single character.

        Note that for this keyword the entire screen is considered a string. So if you want to search
        for the string "something" and it is somewhere other than at the beginning or end of the screen, it
        should be reported as follows: **something**

        The assertion is case sensitive. If you want it to be case insensitive, you can pass the argument ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain Match | **something** |
            | Page Should Not Contain Match | **so???hing** |
            | Page Should Not Contain Match | **someTHING** | ignore_case=True |
            | Page Should Not Contain Match | **something** | error_message=New error message |
        """
        message = error_message
        all_screen = self._read_all_screen()
        if ignore_case:
            txt = txt.lower()
            all_screen = all_screen.lower()
        matcher = Matcher(txt, caseless=False, spaceless=False)
        result = matcher.match(all_screen)
        if result:
            if message is None:
                message = f'There are matches found for "{txt}" pattern'
            raise Exception(message)

    def _read_all_screen(self) -> str:
        """Read all the mainframe screen and return in a single string."""
        full_text = ""
        for ypos in range(24):
            full_text += self.mf.string_get(ypos + 1, 1, 80)
        return full_text

    def _compare_all_list_with_screen_text(
        self,
        list_string: List[str],
        ignore_case: bool,
        message: Optional[str],
        should_match: bool,
    ) -> None:
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self._search_string(string, ignore_case)
            if not should_match and result:
                if message is None:
                    message = f'The string "{string}" was found'
                raise Exception(message)
            elif should_match and not result:
                if message is None:
                    message = f'The string "{string}" was not found'
                raise Exception(message)

    @staticmethod
    def _check_limits(ypos: int, xpos: int):
        """Checks if the user has passed some coordinate y / x greater than that existing in the mainframe"""
        if ypos > 24:
            raise Exception(
                "You have exceeded the y-axis limit of the mainframe screen"
            )
        if xpos > 80:
            raise Exception(
                "You have exceeded the x-axis limit of the mainframe screen"
            )
