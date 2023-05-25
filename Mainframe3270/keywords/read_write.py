import time
from typing import Any, Optional
from robot.api.deco import keyword
from Mainframe3270.librarycomponent import LibraryComponent


class ReadWriteKeywords(LibraryComponent):
    @keyword("Read")
    def read(self, ypos: int, xpos: int, length: int) -> str:
        """Get a string of ``length`` at screen coordinates ``ypos`` / ``xpos``.

        Coordinates are 1 based, as listed in the status area of the terminal.

        Example for read a string in the position y=8 / x=10 of a length 15:
            | ${value} | Read | 8 | 10 | 15 |
        """
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
