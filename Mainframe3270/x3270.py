import os
import re
import shlex
import time
from datetime import timedelta
from os import name as os_name
from typing import Any, List, Optional, Union

# fmt: off
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import (ConnectionCache, secs_to_timestr,  timestr_to_secs)

# fmt: on
from .py3270 import Emulator


class X3270(object):
    def __init__(
        self,
        visible: bool,
        timeout: timedelta,
        wait_time: timedelta,
        wait_time_after_write: timedelta,
        img_folder: str,
        model
    ) -> None:
        self.visible = visible
        self.timeout = self._convert_timeout(timeout)
        self.wait = self._convert_timeout(wait_time)
        self.wait_write = self._convert_timeout(wait_time_after_write)
        self.imgfolder = img_folder
        self.cache = ConnectionCache()
        self.model = model
        # Try Catch to run in Pycharm, and make a documentation in libdoc with no error
        try:
            self.output_folder = BuiltIn().get_variable_value("${OUTPUT DIR}")
        except RobotNotRunningError:
            self.output_folder = os.getcwd()

    @property
    def mf(self) -> Emulator:
        return self.cache.current

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
        alias: Optional[str] = None,
    ) -> int:
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

        This keyword returns the index of the opened connection, which can be used to reference the connection when switching between connections
        using the `Switch Connection` keyword. For more information on opening and switching between multiple connections,
        please refer to the `Concurrent Connections` section.

        Example:
            | Open Connection | Hostname |
            | Open Connection | Hostname | LU=LUname |
            | Open Connection | Hostname | port=992 |
            | @{extra_args}   | Create List | -accepthostname | myhost.com | -cafile | ${CURDIR}/cafile.crt |
            | Append To List  | ${extra_args} | -port | 992 |
            | Open Connection | Hostname | extra_args=${extra_args} |
            | Open Connection | Hostname | extra_args=${CURDIR}/argfile.txt |
            | Open Connection | Hostname | alias=my_first_connection |
        """
        extra_args = self._process_args(extra_args)
        model = self._get_model_from_list_or_file(extra_args)
        connection = Emulator(self.visible, self.timeout, extra_args, model or self.model)
        host_string = f"{LU}@{host}" if LU else host
        if self._port_in_extra_args(extra_args):
            if port != 23:
                logger.warn(
                    "The connection port has been specified both in the `port` argument and in `extra_args`. "
                    "The port specified in `extra_args` will take precedence over the `port` argument. "
                    "To avoid this warning, you can either remove the port command-line option from `extra_args`, "
                    "or leave the `port` argument at its default value of 23."
                )
            connection.connect(host_string)
        else:
            connection.connect(f"{host_string}:{port}")
        return self.cache.register(connection, alias)

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

    def _get_model_from_list_or_file(self, list_or_file):
        pattern = re.compile(r"[wcxs3270.*]+model:\s*([327892345E-]+)")
        match = None
        if isinstance(list_or_file, list):
            match = pattern.findall(str(list_or_file))
        elif isinstance(list_or_file, os.PathLike) or isinstance(list_or_file, str):
            with open(list_or_file) as file:
                match = pattern.findall(file.read())
        return None if not match else match[-1]

    def _port_in_extra_args(self, args) -> bool:
        if not args:
            return False
        pattern = re.compile(r"[wcxs3270.*-]+port[:]{0,1}")
        if pattern.search(str(args)):
            return True
        return False

    @keyword("Open Connection From Session File")
    def open_connection_from_session_file(
        self, session_file: os.PathLike, alias: Optional[str] = None
    ) -> int:
        """Create a connection to an IBM3270 mainframe using a [https://x3270.miraheze.org/wiki/Session_file|session file].

        The session file contains [https://x3270.miraheze.org/wiki/Category:Resources|resources (settings)] for a specific host session.
        The only mandatory setting required to establish the connection is the [https://x3270.miraheze.org/wiki/Hostname_resource|hostname resource].

        This keyword is an alternative to `Open Connection`. Please note that the Robot-Framework-Mainframe-3270-Library
        currently only supports model "2". Specifying any other model will result in a failure.

        For more information on session file syntax and detailed examples, please consult the [https://x3270.miraheze.org/wiki/Session_file|x3270 wiki].

        This keyword returns the index of the opened connection, which can be used to reference the connection when switching between connections
        using the `Switch Connection` keyword. For more information on opening and switching between multiple connections,
        please refer to the `Concurrent Connections` section.

        Example:
        | Open Connection From Session File | ${CURDIR}/session.wc3270 |

        where the content of `session.wc3270` is:
        | wc3270.hostname: myhost.com:23
        | wc3270.model: 2
        """
        self._check_session_file_extension(session_file)
        self._check_contains_hostname(session_file)
        model = self._get_model_from_list_or_file(session_file)
        if os_name == "nt" and self.visible:
            connection = Emulator(self.visible, self.timeout, model=model or self.model)
            connection.connect(str(session_file))
        else:
            connection = Emulator(self.visible, self.timeout, [str(session_file)], model or self.model)
        return self.cache.register(connection, alias)

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

    @keyword("Switch Connection")
    def switch_connection(self, alias_or_index: Union[str, int]):
        """Switch the current to the one identified by index or alias. Indices are returned from
        and aliases can be optionally provided to the `Open Connection` and `Open Connection From Session File`
        keywords.

        For more information on opening and switching between multiple connections,
        please refer to the `Concurrent Connections` section.

        Examples:
        | Open Connection   | Hostname | alias=first  |
        | Open Connection   | Hostname | alias=second | # second is now the current connection |
        | Switch Connection | first    |              | # first is now the current connection  |
        """
        self.cache.switch(alias_or_index)

    @keyword("Close Connection")
    def close_connection(self) -> None:
        """Close the current connection."""
        self.mf.terminate()

    @keyword("Close All Connections")
    def close_all_connections(self) -> None:
        """Close all currently opened connections."""
        self.cache.close_all("terminate")

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
            Emulator()._check_limits(ypos, xpos)
            Emulator().send_string(txt, ypos, xpos)
        else:
            Emulator().send_string(txt)
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
            result = Emulator()._search_string(str(txt))
            if result:
                return txt
        raise Exception(f'String "{txt}" not found in {secs_to_timestr(timeout)}')

