import time
from datetime import timedelta
from robot.api.deco import keyword
from robot.utils import secs_to_timestr
from Mainframe3270.librarycomponent import LibraryComponent
from Mainframe3270.utils import convert_timeout


class WaitAndTimeoutKeywords(LibraryComponent):
    @keyword("Change Timeout")
    def change_timeout(self, seconds: timedelta) -> None:
        """
        Change the timeout for connection in seconds.

        Example:
            | Change Timeout | 3 seconds |
        """
        self.timeout = convert_timeout(seconds)

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
            | Change Wait Time | 0.5 |
            | Change Wait Time | 200 milliseconds |
            | Change Wait Time | 0:00:01.500 |
        """
        self.wait_time = convert_timeout(wait_time)

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
            | Change Wait Time After Write | 1 |
            | Change Wait Time After Write | 0.5 seconds |
            | Change Wait Time After Write | 0:00:02 |
        """
        self.wait_time_after_write = convert_timeout(wait_time_after_write)

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

    @keyword("Wait Until String")
    def wait_until_string(self, txt: str, timeout: timedelta = timedelta(seconds=5)) -> str:
        """Wait until a string exists on the mainframe screen to perform the next step. If the string does not appear
        in 5 seconds, the keyword will raise an exception. You can define a different timeout.

        Example:
            | Wait Until String | something |
            | Wait Until String | something | 10 |
            | Wait Until String | something | 15 s |
            | Wait Until String | something | 0:00:15 |
        """
        timeout = convert_timeout(timeout)
        max_time = time.time() + timeout  # type: ignore
        while time.time() < max_time:
            result = self.mf.search_string(str(txt))
            if result:
                return txt
        raise Exception(f'String "{txt}" not found in {secs_to_timestr(timeout)}')
