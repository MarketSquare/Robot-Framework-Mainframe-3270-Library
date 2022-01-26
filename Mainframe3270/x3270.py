import os
import re
import socket
import time

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import Matcher

from .py3270 import Emulator


class x3270(object):
    def __init__(self, visible, timeout, wait_time, wait_time_after_write, img_folder):
        self.lu = None
        self.host = None
        self.port = None
        self.credential = None
        self.imgfolder = img_folder
        # Try Catch to run in Pycharm, and make a documentation in libdoc with no error
        try:
            self.output_folder = BuiltIn().get_variable_value("${OUTPUT DIR}")
        except RobotNotRunningError as rnrex:
            if "Cannot access execution context" in str(rnrex):
                self.output_folder = os.getcwd()
            else:
                raise RobotNotRunningError()
        except Exception as e:
            raise AssertionError(e)
        self.wait = float(wait_time)
        self.wait_write = float(wait_time_after_write)
        self.timeout = int(timeout)
        self.visible = visible
        self.mf = None

    @keyword("Change Timeout")
    def change_timeout(self, seconds):
        """Change the timeout for connection in seconds."""
        self.timeout = float(seconds)

    @keyword("Open Connection")
    def open_connection(self, host, LU=None, port=23, extra_args=None):
        """Create a connection with IBM3270 mainframe with the default port 23. To make a connection with the mainframe
        you only must inform the Host. You can pass the Logical Unit Name and the Port as optional.

        If you wish, you can provide further configuration data to ``extra_args``. ``extra_args`` takes in a list,
        or a path to a file, containing [https://x3270.miraheze.org/wiki/Category:Command-line_options|x3270 command line options].
        Entries in the argfile can be on one line or multiple lines. Lines starting with "#" are considered comments.
        | # example_argfile_oneline.txt
        | --accepthostname myhost.com

        | # example_argfile_multiline.txt
        | --accepthostname myhost.com
        | # this is a comment
        | --charset french

        Please make sure the arguments you are providing are available for your specific x3270 application and version.

        Example:
            | Open Connection | Hostname |
            | Open Connection | Hostname | LU=LUname |
            | Open Connection | Hostname | port=992 |
            | ${extra_args}   | Create List | --accepthostname | myhost.com | --cafile | ${CURDIR}/cafile.crt |
            | Open Connection | Hostname | extra_args=${extra_args} |
            | Open Connection | Hostname | extra_args=${CURDIR}/argfile.txt |
        """
        self.host = host
        self.lu = LU
        self.port = port
        if self.lu:
            self.credential = "%s@%s:%s" % (self.lu, self.host, self.port)
        else:
            self.credential = "%s:%s" % (self.host, self.port)
        if self.mf:
            self.close_connection()
        self.mf = Emulator(
            visible=bool(self.visible), timeout=int(self.timeout), extra_args=extra_args
        )
        self.mf.connect(self.credential)

    @keyword("Close Connection")
    def close_connection(self):
        """Disconnect from the host."""
        try:
            self.mf.terminate()
        except socket.error:
            pass
        self.mf = None

    @keyword("Change Wait Time")
    def change_wait_time(self, wait_time):
        """To give time for the mainframe screen to be "drawn" and receive the next commands, a "wait time" has been
        created, which by default is set to 0.5 seconds. This is a sleep applied AFTER the follow keywords:

        `Execute Command`
        `Send Enter`
        `Send PF`
        `Write`
        `Write in position`

        If you want to change this value just use this keyword passing the time in seconds.

        Examples:
            | Change Wait Time | 0.1 |
            | Change Wait Time | 2 |
        """
        self.wait = float(wait_time)

    @keyword("Change Wait Time After Write")
    def change_wait_time_after_write(self, wait_time_after_write):
        """To give the user time to see what is happening inside the mainframe, a "change wait time after write" has
        been created, which by default is set to 0 seconds. This is a sleep applied AFTER the string sent in this
        keywords:

        `Write`
        `Write Bare`
        `Write in position`
        `Write Bare in position`

        If you want to change this value just use this keyword passing the time in seconds.

        Note: This keyword is useful for debug purpose

        Examples:
            | Change Wait Time After Write | 0.5 |
            | Change Wait Time After Write | 2 |
        """
        self.wait_write = float(wait_time_after_write)

    @keyword("Read")
    def read(self, ypos, xpos, length):
        """Get a string of "length" at screen co-ordinates "ypos"/"xpos".

        Co-ordinates are 1 based, as listed in the status area of the terminal.

        Example for read a string in the position y=8 / x=10 of a length 15:
            | ${value} | Read | 8 | 10 | 15 |
        """
        self._check_limits(ypos, xpos)
        # Checks if the user has passed a length that will be larger than the x limit of the screen.
        if int(xpos) + int(length) > (80 + 1):
            raise Exception(
                "You have exceeded the x-axis limit of the mainframe screen"
            )
        string = self.mf.string_get(int(ypos), int(xpos), int(length))
        return str(string)

    @keyword("Read All Screen")
    def read_all_screen(self):
        """Reads the current screen and returns all content in one string.

        Example:
            | ${content} | Read All Screen |
        """
        return self._read_all_screen()

    @keyword("Execute Command")
    def execute_command(self, cmd):
        """Execute an [http://x3270.bgp.nu/wc3270-man.html#Actions|x3270 command].

        Examples:
            | Execute Command | Enter |
            | Execute Command | Home |
            | Execute Command | Tab |
            | Execute Command | PF(1) |
        """
        self.mf.exec_command((str(cmd)).encode("utf-8"))
        time.sleep(self.wait)

    @keyword("Set Screenshot Folder")
    def set_screenshot_folder(self, path):
        r"""Set a folder to keep the html files generated by the `Take Screenshot` keyword.

        Example:
            | Set Screenshot Folder | C:\\Temp\\Images |
        """
        if os.path.exists(os.path.normpath(os.path.join(self.output_folder, path))):
            self.imgfolder = path
        else:
            logger.error('Given screenshots path "%s" does not exist' % path)
            logger.warn('Screenshots will be saved in "%s"' % self.imgfolder)

    @keyword("Take Screenshot")
    def take_screenshot(self, height="410", width="670"):
        """Generate a screenshot of the IBM 3270 Mainframe in a html format. The
        default folder is the log folder of RobotFramework, if you want change see the `Set Screenshot Folder`.

        The Screenshot is printed in a iframe log, with the values of height=410 and width=670, you
        can change this values passing them from the keyword.

        Examples:
            | Take Screenshot |
            | Take Screenshot | height=500 | width=700 |
        """
        filename_prefix = "screenshot"
        extension = "html"
        filename_sufix = str(int(round(time.time() * 1000)))
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

    @keyword("Wait Field Detected")
    def wait_field_detected(self):
        """Wait until the screen is ready, the cursor has been positioned
        on a modifiable field, and the keyboard is unlocked.

        Sometimes the server will "unlock" the keyboard but the screen
        will not yet be ready.  In that case, an attempt to read or write to the
        screen will result in a 'E' keyboard status because we tried to read from
        a screen that is not yet ready.

        Using this method tells the client to wait until a field is
        detected and the cursor has been positioned on it.
        """
        self.mf.wait_for_field()

    @keyword("Delete Char")
    def delete_char(self, ypos=None, xpos=None):
        """Delete character under cursor. If you want to delete a character that is in
        another position, simply pass the coordinates "ypos"/"xpos".

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Examples:
            | Delete Char |
            | Delete Char | ypos=9 | xpos=25 |
        """
        if ypos is not None and xpos is not None:
            self.mf.move_to(int(ypos), int(xpos))
        self.mf.exec_command(b"Delete")

    @keyword("Delete Field")
    def delete_field(self, ypos=None, xpos=None):
        """Delete a entire contents in field at current cursor location and positions
        cursor at beginning of field. If you want to delete a field that is in
        another position, simply pass the coordinates "ypos"/"xpos" of any part of the field.

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Examples:
            | Delete Field |
            | Delete Field | ypos=12 | xpos=6 |
        """
        if ypos is not None and xpos is not None:
            self.mf.move_to(int(ypos), int(xpos))
        self.mf.exec_command(b"DeleteField")

    @keyword("Send Enter")
    def send_enter(self):
        """Send a Enter to the screen."""
        self.mf.send_enter()
        time.sleep(self.wait)

    @keyword("Move Next Field")
    def move_next_field(self):
        """Move the cursor to the next input field. Equivalent to pressing the Tab key."""
        self.mf.exec_command(b"Tab")

    @keyword("Move Previous Field")
    def move_previous_field(self):
        """Move the cursor to the previous input field. Equivalent to pressing the Shift+Tab keys."""
        self.mf.exec_command(b"BackTab")

    @keyword("Send PF")
    def send_PF(self, PF):
        """Send a Program Function to the screen.

        Example:
               | Send PF | 3 |
        """
        self.mf.exec_command(("PF(" + str(PF) + ")").encode("utf-8"))
        time.sleep(self.wait)

    @keyword("Write")
    def write(self, txt):
        """Send a string to the screen at the current cursor location *and a Enter.*

        Example:
            | Write | something |
        """
        self._write(txt, enter="1")

    @keyword("Write Bare")
    def write_bare(self, txt):
        """Send only the string to the screen at the current cursor location.

        Example:
            | Write Bare | something |
        """
        self._write(txt)

    @keyword("Write In Position")
    def write_in_position(self, txt, ypos, xpos):
        """Send a string to the screen at screen co-ordinates "ypos"/"xpos" and a Enter.

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Write in Position | something | 9 | 11 |
        """
        self._write(txt, ypos=ypos, xpos=xpos, enter="1")

    @keyword("Write Bare In Position")
    def write_bare_in_position(self, txt, ypos, xpos):
        """Send only the string to the screen at screen co-ordinates "ypos"/"xpos".

        Co-ordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Write Bare in Position | something | 9 | 11 |
        """
        self._write(txt, ypos=ypos, xpos=xpos)

    def _write(self, txt, ypos=None, xpos=None, enter="0"):
        txt = txt.encode("unicode_escape")
        if ypos is not None and xpos is not None:
            self._check_limits(int(ypos), int(xpos))
            self.mf.move_to(int(ypos), int(xpos))
        if not isinstance(txt, (list, tuple)):
            txt = [txt]
        [self.mf.send_string(el) for el in txt if el != ""]
        time.sleep(self.wait_write)
        for i in range(int(enter)):
            self.mf.send_enter()
            time.sleep(self.wait)

    @keyword("Wait Until String")
    def wait_until_string(self, txt, timeout=5):
        """Wait until a string exists on the mainframe screen to perform the next step. If the string not appear on
        5 seconds the keyword will raise a exception. You can define a different timeout.

        Example:
            | Wait Until String | something |
            | Wait Until String | something | timeout=10 |
        """
        max_time = time.ctime(int(time.time()) + int(timeout))
        while time.ctime(int(time.time())) < max_time:
            result = self._search_string(str(txt))
            if result:
                return txt
        raise Exception(
            'String "' + txt + '" not found in ' + str(timeout) + " seconds"
        )

    def _search_string(self, string, ignore_case=False):
        """Search if a string exists on the mainframe screen and return True or False."""

        def __read_screen(string, ignore_case):
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
    def page_should_contain_string(self, txt, ignore_case=False, error_message=None):
        """Search if a given string exists on the mainframe screen.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True}
        and you can edit the raise exception message with error_message.

        Example:
            | Page Should Contain String | something |
            | Page Should Contain String | someTHING | ignore_case=${True} |
            | Page Should Contain String | something | error_message=New error message |
        """
        message = 'The string "' + txt + '" was not found'
        if error_message:
            message = error_message
        if ignore_case:
            txt = str(txt).lower()
        result = self._search_string(txt, ignore_case)
        if not result:
            raise Exception(message)
        logger.info('The string "' + txt + '" was found')

    @keyword("Page Should Not Contain String")
    def page_should_not_contain_string(
        self, txt, ignore_case=False, error_message=None
    ):
        """Search if a given string NOT exists on the mainframe screen.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True}
        and you can edit the raise exception message with error_message.

        Example:
            | Page Should Not Contain String | something |
            | Page Should Not Contain String | someTHING | ignore_case=${True} |
            | Page Should Not Contain String | something | error_message=New error message |
        """
        message = 'The string "' + txt + '" was found'
        if error_message:
            message = error_message
        if ignore_case:
            txt = str(txt).lower()
        result = self._search_string(txt, ignore_case)
        if result:
            raise Exception(message)

    @keyword("Page Should Contain Any String")
    def page_should_contain_any_string(
        self, list_string, ignore_case=False, error_message=None
    ):
        """Search if one of the strings in a given list exists on the mainframe screen.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True}
        and you can edit the raise exception message with error_message.

        Example:
            | Page Should Contain Any String | ${list_of_string} |
            | Page Should Contain Any String | ${list_of_string} | ignore_case=${True} |
            | Page Should Contain Any String | ${list_of_string} | error_message=New error message |
        """
        message = 'The strings "' + str(list_string) + '" was not found'
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
        self, list_string, ignore_case=False, error_message=None
    ):
        """Fails if one or more of the strings in a given list exists on the mainframe screen. if one or more of the
        string are found, the keyword will raise a exception.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True}
        and you can edit the raise exception message with error_message.

        Example:
            | Page Should Not Contain Any Strings | ${list_of_string} |
            | Page Should Not Contain Any Strings | ${list_of_string} | ignore_case=${True} |
            | Page Should Not Contain Any Strings | ${list_of_string} | error_message=New error message |
        """
        self._compare_all_list_with_screen_text(
            list_string, ignore_case, error_message, should_match=False
        )

    @keyword("Page Should Contain All Strings")
    def page_should_contain_all_strings(
        self, list_string, ignore_case=False, error_message=None
    ):
        """Search if all of the strings in a given list exists on the mainframe screen.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True}
        and you can edit the raise exception message with error_message.

        Example:
            | Page Should Contain All Strings | ${list_of_string} |
            | Page Should Contain All Strings | ${list_of_string} | ignore_case=${True} |
            | Page Should Contain All Strings | ${list_of_string} | error_message=New error message |
        """
        self._compare_all_list_with_screen_text(
            list_string, ignore_case, error_message, should_match=True
        )

    @keyword("Page Should Not Contain All Strings")
    def page_should_not_contain_all_strings(
        self, list_string, ignore_case=False, error_message=None
    ):
        """Fails if one of the strings in a given list exists on the mainframe screen. if one of the string
        are found, the keyword will raise a exception.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True}
        and you can edit the raise exception message with error_message.

        Example:
            | Page Should Not Contain All Strings | ${list_of_string} |
            | Page Should Not Contain All Strings | ${list_of_string} | ignore_case=${True} |
            | Page Should Not Contain All Strings | ${list_of_string} | error_message=New error message |
        """
        message = error_message
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self._search_string(string, ignore_case)
            if result:
                if message is None:
                    message = 'The string "' + string + '" was found'
                raise Exception(message)

    @keyword("Page Should Contain String X Times")
    def page_should_contain_string_x_times(
        self, txt, number, ignore_case=False, error_message=None
    ):
        """Search if the entered string appears the desired number of times on the mainframe screen.

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True} and you
        can edit the raise exception message with error_message.

        Example:
               | Page Should Contain String X Times | something | 3 |
               | Page Should Contain String X Times | someTHING | 3 | ignore_case=${True} |
               | Page Should Contain String X Times | something | 3 | error_message=New error message |
        """
        message = error_message
        number = int(number)
        all_screen = self._read_all_screen()
        if ignore_case:
            txt = str(txt).lower()
            all_screen = str(all_screen).lower()
        number_of_times = all_screen.count(txt)
        if number_of_times != number:
            if message is None:
                message = f'The string "{txt}" was not found "{number}" times, it appears "{number_of_times}" times'
            raise Exception(message)
        logger.info('The string "' + txt + '" was found "' + str(number) + '" times')

    @keyword("Page Should Match Regex")
    def page_should_match_regex(self, regex_pattern):
        r"""Fails if string does not match pattern as a regular expression. Regular expression check is
        implemented using the Python [https://docs.python.org/2/library/re.html|re module]. Python's
        regular expression syntax is derived from Perl, and it is thus also very similar to the syntax used,
        for example, in Java, Ruby and .NET.

        Backslash is an escape character in the test data, and possible backslashes in the pattern must
        thus be escaped with another backslash (e.g. \\d\\w+).
        """
        page_text = self._read_all_screen()
        if not re.findall(regex_pattern, page_text, re.MULTILINE):
            raise Exception('No matches found for "' + regex_pattern + '" pattern')

    @keyword("Page Should Not Match Regex")
    def page_should_not_match_regex(self, regex_pattern):
        r"""Fails if string does match pattern as a regular expression. Regular expression check is
        implemented using the Python [https://docs.python.org/2/library/re.html|re module]. Python's
        regular expression syntax is derived from Perl, and it is thus also very similar to the syntax used,
        for example, in Java, Ruby and .NET.

        Backslash is an escape character in the test data, and possible backslashes in the pattern must
        thus be escaped with another backslash (e.g. \\d\\w+).
        """
        page_text = self._read_all_screen()
        if re.findall(regex_pattern, page_text, re.MULTILINE):
            raise Exception(
                'There are matches found for "' + regex_pattern + '" pattern'
            )

    @keyword("Page Should Contain Match")
    def page_should_contain_match(self, txt, ignore_case=False, error_message=None):
        """Fails unless the given string matches the given pattern.

        Pattern matching is similar as matching files in a shell, and it is always case-sensitive.
        In the pattern, * matches to anything and ? matches to any single character.

        Note that the entire screen is only considered a string for this keyword, so if you want to search
        for the string "something" and it is somewhere other than at the beginning or end of the screen it
        should be reported as follows: **something**

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True} and you
        can edit the raise exception message with error_message.

        Example:
            | Page Should Contain Match | **something** |
            | Page Should Contain Match | **so???hing** |
            | Page Should Contain Match | **someTHING** | ignore_case=${True} |
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
                message = 'No matches found for "' + txt + '" pattern'
            raise Exception(message)

    @keyword("Page Should Not Contain Match")
    def page_should_not_contain_match(self, txt, ignore_case=False, error_message=None):
        """Fails if the given string matches the given pattern.

        Pattern matching is similar as matching files in a shell, and it is always case-sensitive.
        In the pattern, * matches to anything and ? matches to any single character.

        Note that the entire screen is only considered a string for this keyword, so if you want to search
        for the string "something" and it is somewhere other than at the beginning or end of the screen it
        should be reported as follows: **something**

        The search is case sensitive, if you want ignore this you can pass the argument: ignore_case=${True} and you
        can edit the raise exception message with error_message.

        Example:
            | Page Should Not Contain Match | **something** |
            | Page Should Not Contain Match | **so???hing** |
            | Page Should Not Contain Match | **someTHING** | ignore_case=${True} |
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
                message = 'There are matches found for "' + txt + '" pattern'
            raise Exception(message)

    def _read_all_screen(self):
        """Read all the mainframe screen and return in a single string."""
        full_text = ""
        for ypos in range(24):
            line = self.mf.string_get(ypos + 1, 1, 80)
            for char in line:
                if char:
                    full_text += char
        return full_text

    def _compare_all_list_with_screen_text(
        self, list_string, ignore_case, message, should_match
    ):
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self._search_string(string, ignore_case)
            if not should_match and result:
                if message is None:
                    message = 'The string "' + string + '" was found'
                raise Exception(message)
            elif should_match and not result:
                if message is None:
                    message = 'The string "' + string + '" was not found'
                raise Exception(message)

    @staticmethod
    def _check_limits(ypos, xpos):
        """Checks if the user has passed some coordinate y / x greater than that existing in the mainframe"""
        if int(ypos) > 24:
            raise Exception(
                "You have exceeded the y-axis limit of the mainframe screen"
            )
        if int(xpos) > 80:
            raise Exception(
                "You have exceeded the x-axis limit of the mainframe screen"
            )
