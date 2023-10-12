import time
from typing import Optional, Union

from robot.api import logger
from robot.api.deco import keyword

from Mainframe3270.librarycomponent import LibraryComponent


class CommandKeywords(LibraryComponent):
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
        time.sleep(self.wait_time)

    @keyword("Delete Char")
    def delete_char(self, ypos: Optional[int] = None, xpos: Optional[int] = None) -> None:
        """Delete the character under the cursor. If you want to delete a character that is in
        another position, simply pass the coordinates ``ypos`` / ``xpos``.

        Coordinates are 1 based, as listed in the status area of the terminal.

        Example:
            | Delete Char |
            | Delete Char | ypos=9 | xpos=25 |
        """
        if ypos and xpos:
            self.mf.move_to(ypos, xpos)
        self.mf.exec_command(b"Delete")

    @keyword("Delete Field")
    def delete_field(self, ypos: Optional[int] = None, xpos: Optional[int] = None) -> None:
        """Delete the entire content of a field at the current cursor location and positions
        the cursor at beginning of field. If you want to delete a field that is in
        another position, simply pass the coordinates ``ypos`` / ``xpos`` of any part in the field.

        Coordinates are 1 based, as listed in the status area of the terminal.

        Example:
            | Delete Field |
            | Delete Field | ypos=12 | xpos=6 |
        """
        if ypos and xpos:
            self.mf.move_to(ypos, xpos)
        self.mf.delete_field()

    @keyword("Send Enter")
    def send_enter(self) -> None:
        """
        Send an Enter to the screen.
        """
        self.mf.send_enter()
        time.sleep(self.wait_time)

    @keyword("Move Next Field")
    def move_next_field(self) -> None:
        """
        Move the cursor to the next input field. Equivalent to pressing the Tab key.
        """
        self.mf.exec_command(b"Tab")

    @keyword("Move Previous Field")
    def move_previous_field(self) -> None:
        """
        Move the cursor to the previous input field. Equivalent to pressing the Shift+Tab keys.
        """
        self.mf.exec_command(b"BackTab")

    @keyword("Send PF")
    def send_pf(self, pf: str) -> None:
        """Send a Program Function to the screen.

        Example:
            | Send PF | 3 |
        """
        self.mf.exec_command("PF({0})".format(pf).encode("utf-8"))
        time.sleep(self.wait_time)

    @keyword("Get Cursor Position")
    def get_cursor_position(self, mode: str = "As Tuple") -> Union[tuple, dict]:
        """Returns the current cursor position. The coordinates are 1 based.

        By default, this keyword returns a tuple of integers. However, if you specify the `mode` with the value
        ``"As Dict"`` (case-insensitive), a dictionary in the form of ``{"xpos": int, "ypos": int}`` is returned.

        Example:
            | Get Cursor Position |         | # Returns a position like (1, 1) |
            | Get Cursor Position | As Dict | # Returns a position like {"xpos": 1, "ypos": 1} |

        """
        result = self.mf.get_cursor_position()
        if mode.lower() == "as dict":
            return {"ypos": result[0], "xpos": result[1]}
        elif mode.lower() == "as tuple":
            return result
        else:
            logger.warn('"mode" should be either "as dict" or "as tuple". Returning the result as tuple')
            return result
