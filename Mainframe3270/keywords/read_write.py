import time
from typing import Any, Optional
from robot.api.deco import keyword
from Mainframe3270.librarycomponent import LibraryComponent
from Mainframe3270.utils import ResultMode, prepare_positions_as


class ReadWriteKeywords(LibraryComponent):
    @keyword("Read")
    def read(self, ypos: int, xpos: int, length: int) -> str:
        """Get a string of ``length`` at screen coordinates ``ypos`` / ``xpos``.

        Coordinates are 1 based, as listed in the status area of the terminal.

        Example for read a string in the position y=8 / x=10 of a length 15:
            | ${value} | Read | 8 | 10 | 15 |
        """
        return self.mf.string_get(ypos, xpos, length)

    @keyword("Read From Current Position")
    def read_from_current_position(self, length: int):
        """Similar to `Read`, however this keyword only takes `length` as an argument
        to get a string of length from the current cursor position."""
        ypos, xpos = self.mf.get_current_position()
        return self.mf.string_get(ypos, xpos, length)

    @keyword("Read All Screen")
    def read_all_screen(self) -> str:
        """Read the current screen and returns all content in one string.

        This is useful if your automation scripts should take different routes depending
        on a message shown on the screen.

        Example:
            | ${screen} | Read All Screen |
            | IF | 'certain text' in '''${screen}''' |
            | | Do Something |
            | ELSE | |
            | | Do Something Else |
            | END | |
        """
        return self.mf.read_all_screen()

    @keyword("Get String Positions")
    def get_string_positions(self, string: str, mode: ResultMode = ResultMode.As_Tuple, ignore_case: bool = False):
        """Returns a list of tuples of ypos and xpos for the position where the `string` was found,
        or an empty list if it was not found.

        If you specify the `mode` with the value `"As Dict"` (case-insensitive),
        a list of dictionaries in the form of ``[{"xpos": int, "ypos": int}]`` is returned.

        If `ignore_case` is set to `True`, then the search is done case-insensitively.

        Example:
            | ${positions} | Get String Positions | Abc |         | # Returns a list like [(1, 8)] |
            | ${positions} | Get String Positions | Abc | As Dict | # Returns a list like [{"ypos": 1, "xpos": 8}] |
        """
        positions = self.mf.get_string_positions(string, ignore_case)
        return prepare_positions_as(positions, mode)

    @keyword("Get String Positions Only After")
    def get_string_positions_only_after(
        self,
        ypos: int,
        xpos: int,
        string: str,
        mode: ResultMode = ResultMode.As_Tuple,
        ignore_case: bool = False,
    ):
        """Returns a list of tuples of ypos and xpos for the position where the `string` was found,
        but only after the specified ypos/xpos coordinates. If it is not found an empty list is returned.

        If you specify the `mode` with the value `"As Dict"` (case-insensitive),
        a list of dictionaries in the form of ``[{"xpos": int, "ypos": int}]`` is returned.

        If `ignore_case` is set to `True`, then the search is done case-insensitively.

        Example:
            | ${positions} | Get String Positions Only After | 5 | 4 | Abc |         | # Returns a list like [(5, 5)] |
            | ${positions} | Get String Positions Only After | 5 | 4 | Abc | As Dict | # Returns a list like [{"ypos": 5, "xpos": 5}] |
        """
        self.mf.check_limits(ypos, xpos)
        positions = self.mf.get_string_positions(string, ignore_case)
        filtered_positions = [position for position in positions if position > (ypos, xpos)]
        return prepare_positions_as(filtered_positions, mode)

    @keyword("Get String Positions Only Before")
    def get_string_positions_only_before(
        self,
        ypos: int,
        xpos: int,
        string: str,
        mode: ResultMode = ResultMode.As_Tuple,
        ignore_case: bool = False,
    ):
        """Returns a list of tuples of ypos and xpos for the position where the `string` was found,
        but only before the specified ypos/xpos coordinates. If it is not found an empty list is returned.

        If you specify the `mode` with the value `"As Dict"` (case-insensitive),
        a list of dictionaries in the form of ``[{"xpos": int, "ypos": int}]`` is returned.

        If `ignore_case` is set to `True`, then the search is done case-insensitively.

        Example:
            | ${positions} | Get String Positions Only Before | 11 | 20 | Abc |         | # Returns a list like [(11, 19)] |
            | ${positions} | Get String Positions Only Before | 11 | 20 | Abc | As Dict | # Returns a list like [{"ypos": 11, "xpos": 19}] |
        """
        self.mf.check_limits(ypos, xpos)
        positions = self.mf.get_string_positions(string, ignore_case)
        filtered_positions = [position for position in positions if position < (ypos, xpos)]
        return prepare_positions_as(filtered_positions, mode)

    @keyword("Write")
    def write(self, txt: str) -> None:
        """Send a string *and Enter* to the screen at the current cursor location.

        Example:
            | Write | something |
        """
        self._write(txt, enter=True)

    @keyword("Write Bare")
    def write_bare(self, txt: str) -> None:
        """Send only the string to the screen at the current cursor location.

        Example:
            | Write Bare | something |
        """
        self._write(txt)

    @keyword("Write In Position")
    def write_in_position(self, txt: str, ypos: int, xpos: int) -> None:
        """Send a string *and Enter* to the screen at screen coordinates ``ypos`` / ``xpos``.

        Coordinates are 1 based, as listed in the status area of the
        terminal.

        Example:
            | Write in Position | something | 9 | 11 |
        """
        self._write(txt, ypos, xpos, enter=True)

    @keyword("Write Bare In Position")
    def write_bare_in_position(self, txt: str, ypos: int, xpos: int):
        """Send only the string to the screen at screen coordinates ``ypos`` / ``xpos``.

        Coordinates are 1 based, as listed in the status area of the
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
        enter: bool = False,
    ) -> None:
        txt = txt.encode("unicode_escape")
        if ypos and xpos:
            self.mf.send_string(txt, ypos, xpos)
        else:
            self.mf.send_string(txt)
        time.sleep(self.wait_time_after_write)
        if enter:
            self.mf.send_enter()
            time.sleep(self.wait_time)
