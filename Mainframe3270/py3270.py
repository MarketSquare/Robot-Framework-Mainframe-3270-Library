import errno
import logging
import math
import re
import socket
import subprocess
import time
import warnings
from abc import ABC, abstractmethod
from contextlib import closing
from os import name as os_name
from robot.utils import seq2str

log = logging.getLogger(__name__)
"""
    Python 3+ note: unicode strings should be used when communicating with the Emulator methods.
    utf-8 is used internally when reading from or writing to the 3270 emulator (this includes
    reading lines, constructing data to write, reading statuses).
"""


class CommandError(Exception):
    pass


class TerminatedError(Exception):
    pass


class WaitError(Exception):
    pass


class KeyboardStateError(Exception):
    pass


class FieldTruncateError(Exception):
    pass


class Command(object):
    """
    Represents a x3270 script command
    """

    def __init__(self, app, cmdstr):
        if isinstance(cmdstr, str):
            warnings.warn("Commands should be byte strings", stacklevel=3)
            cmdstr = cmdstr.encode("utf-8")
        self.app = app
        self.cmdstr = cmdstr
        self.status_line = None
        self.data = []

    def execute(self):
        self.app.write(self.cmdstr + b"\n")

        # x3270 puts data lines (if any) on stdout prefixed with 'data: '
        # followed by two more lines without the prefix.
        # 1: status of the emulator
        # 2: 'ok' or 'error' indicating whether the command succeeded or failed
        while True:
            line = self.app.readline()
            # log.debug('stdout line: %s', line.rstrip())       # commented line to reduce log size
            if not line.startswith("data:".encode("ascii")):
                # ok, we are at the status line
                self.status_line = line.rstrip()
                result = self.app.readline().rstrip()
                # log.debug('result line: %s', result)          # commented line to reduce log size
                return self.handle_result(result.decode("utf-8"))

            # remove the 'data: ' prefix and trailing newline char(s) and store
            self.data.append(line[6:].rstrip("\n\r".encode("utf-8")))

    def handle_result(self, result):
        # should receive 'ok' for almost everything, but Quit returns a '' for
        # some reason
        if result == "" and self.cmdstr == b"Quit":
            return
        if result == "ok":
            return
        if result != "error":
            raise ValueError('expected "ok" or "error" result, but received: {0}'.format(result))

        msg = b"[no error message]"
        if self.data:
            msg = "".encode("utf-8").join(self.data).rstrip()
        raise CommandError(msg.decode("utf-8"))


class Status(object):
    """
    Represents a status line as returned by x3270 following a command
    """

    def __init__(self, status_line):
        if not status_line:
            status_line = (" " * 12).encode("utf-8")
        parts = status_line.split(" ".encode("utf-8"))
        self.as_string = status_line.rstrip().decode("utf-8")
        self.keyboard = parts[0] or None
        self.screen_format = parts[1] or None
        self.field_protection = parts[2] or None
        self.connection_state = parts[3] or None
        self.emulator_mode = parts[4] or None
        self.model_number = parts[5] or None
        self.row_number = parts[6] or None
        self.col_number = parts[7] or None
        self.cursor_row = parts[8] or None
        self.cursor_col = parts[9] or None
        self.window_id = parts[10] or None
        self.exec_time = parts[11] or None

    def __str__(self):
        return "STATUS: {0}".format(self.as_string)


class ExecutableApp(ABC):
    @property
    @abstractmethod
    def executable(self):
        pass

    @property
    @abstractmethod
    def args(self):
        pass

    def __init__(self, extra_args=None, model="2"):
        self.args = self._get_executable_app_args(extra_args, model)
        self.sp = None
        self.spawn_app()

    def spawn_app(self):
        args = [self.executable] + self.args
        self.sp = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def connect(self, host):
        """this is a no-op for all but wc3270"""
        return False

    def close(self):
        pass

    def write(self, data):
        self.sp.stdin.write(data)
        self.sp.stdin.flush()

    def readline(self):
        return self.sp.stdout.readline()

    def _get_executable_app_args(self, extra_args, model):
        return self.__class__.args + ["-xrm", f"*model: {model}"] + (extra_args or [])


class x3270App(ExecutableApp):
    executable = "x3270"
    # Per Paul Mattes, in the first days of x3270, there were servers that
    # would unlock the keyboard before they had processed the command. To
    # work around that, when AID commands are sent, there is a 350ms delay
    # before the command returns. This arg turns that feature off for
    # performance reasons.
    args = ["-xrm", "x3270.unlockDelay: False", "-script"]


class s3270App(ExecutableApp):
    executable = "s3270"
    # see notes for args in x3270App
    args = ["-xrm", "s3270.unlockDelay: False"]


class NotConnectedException(Exception):
    pass


class wc3270App(ExecutableApp):
    executable = "wc3270"
    # see notes for args in x3270App
    args = ["-xrm", "wc3270.unlockDelay: False"]

    def __init__(self, extra_args=None, model="2"):
        self.args = self._get_executable_app_args(extra_args, model)
        self.sp = None
        self.socket_fh = None
        self.script_port = self._get_free_port()

    def _get_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("127.0.0.1", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def connect(self, host):
        self.spawn_app(host)
        self.make_socket()
        return True

    def close(self):
        # failing to close the socket ourselves will result in a ResourceWarning
        self.socket.close()

    def spawn_app(self, host):
        args = ["start", "/wait", self.executable] + self.args
        args.extend(["-scriptport", str(self.script_port), host])
        self.sp = subprocess.Popen(
            args,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def make_socket(self):
        self.socket = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        count = 0
        while count < 15:
            try:
                sock.connect(("127.0.0.1", self.script_port))
                break
            except socket.error as e:
                log.warning(e)
                if e.errno != errno.ECONNREFUSED:
                    raise
                time.sleep(1)
                count += 1
        # open a file handle for the socket that can both read and write, using bytestrings
        self.socket_fh = sock.makefile(mode="rwb")

    def write(self, data):
        if self.socket_fh is None:
            raise NotConnectedException
        self.socket_fh.write(data)
        self.socket_fh.flush()

    def readline(self):
        if self.socket_fh is None:
            raise NotConnectedException
        return self.socket_fh.readline()


class ws3270App(ExecutableApp):
    executable = "ws3270"
    # see notes for args in x3270App
    args = ["-xrm", "ws3270.unlockDelay: False"]


class Emulator(object):
    """
    Represents an x/s3270 emulator subprocess and provides an API for interacting
    with it.
    """

    _MODEL_TYPES = {
        "2": "2",
        "3278-2": "2",
        "3278-2-E": "2",
        "3279-2": "2",
        "3279-2-E": "2",
        "3": "3",
        "3278-3": "3",
        "3278-3-E": "3",
        "3279-3": "3",
        "3279-3-E": "3",
        "4": "4",
        "3278-4": "4",
        "3278-4-E": "4",
        "3279-4": "4",
        "3279-4-E": "4",
        "5": "5",
        "3278-5": "5",
        "3278-5-E": "5",
        "3279-5": "5",
        "3279-5-E": "5",
    }

    _MODEL_DIMENSIONS = {
        "2": {
            "rows": 24,
            "columns": 80,
        },
        "3": {
            "rows": 32,
            "columns": 80,
        },
        "4": {
            "rows": 43,
            "columns": 80,
        },
        "5": {
            "rows": 27,
            "columns": 132,
        },
    }

    def __init__(self, visible=False, timeout=30, extra_args=None, model="2"):
        """
        Create an emulator instance

        `visible` controls which executable will be used.
        `timeout` controls the timeout parameter to any Wait() command sent
            to x3270.
        `extra_args` allows sending parameters to the emulator executable
        """
        self.model = model
        self.model_dimensions = self._set_model_dimensions(model)
        self.app = self.create_app(visible, extra_args, model)
        self.is_terminated = False
        self.status = Status(None)
        self.timeout = timeout
        self.last_host = None

    def _set_model_dimensions(self, model):
        try:
            model_type = Emulator._MODEL_TYPES[model]
        except KeyError:
            raise ValueError(
                f"Model should be one of {seq2str(Emulator._MODEL_TYPES.keys()).replace('and', 'or')}, "
                f"but was '{model}'."
            )
        return Emulator._MODEL_DIMENSIONS[model_type]

    def create_app(self, visible, extra_args, model):
        if os_name == "nt":
            if visible:
                return wc3270App(extra_args, model)
            return ws3270App(extra_args, model)
        if visible:
            return x3270App(extra_args, model)
        return s3270App(extra_args, model)

    def exec_command(self, cmdstr):
        """
        Execute a x3270 command

        `cmdstr` gets sent directly to the x3270 subprocess on its stdin.
        """
        if self.is_terminated:
            raise TerminatedError("This Emulator instance has been terminated")

        # log.debug('sending command: %s', cmdstr)             # commented line to reduce log size
        c = Command(self.app, cmdstr)
        # start = time.time()                                  # unnecessary variable if the log is commented out.
        c.execute()
        # elapsed = time.time() - start                        # unnecessary variable if the log is commented out.
        # log.debug('elapsed execution: {0}'.format(elapsed))  # commented line to reduce log size
        self.status = Status(c.status_line)

        return c

    def terminate(self):
        """
        terminates the underlying x3270 subprocess. Once called, this Emulator instance must no longer be used.
        """
        if not self.is_terminated:
            log.debug("terminal client terminated")
            try:
                self.exec_command(b"Quit")
            except BrokenPipeError:
                # x3270 was terminated, since we are just quitting anyway, ignore it.
                pass
            except socket.error as e:
                # if 'was forcibly closed' not in str(e):
                if e.errno != errno.ECONNRESET:
                    raise
                # this can happen because wc3270 closes the socket before
                # the read() can happen, causing a socket error

            self.app.close()

            self.is_terminated = True

    def is_connected(self):
        """
        Return bool indicating connection state
        """
        # need to wrap in try/except b/c of wc3270's socket connection dynamics
        try:
            # this is basically a no-op, but it results in the the current status
            # getting updated
            self.exec_command(b"ignore")

            # connected status is like 'C(192.168.1.1)', disconnected is 'N'
            return self.status.connection_state.startswith(b"C(")
        except NotConnectedException:
            return False

    def connect(self, host):
        """
        Connect to a host
        """
        if not self.app.connect(host):
            command = "Connect({0})".format(host).encode("utf-8")
            self.exec_command(command)
        self.last_host = host

    def reconnect(self):
        """
        Disconnect from the host and re-connect to the same host
        """
        self.exec_command(b"Disconnect")
        self.connect(self.last_host)

    def wait_for_field(self):
        """
        Wait until the screen is ready, the cursor has been positioned
        on a modifiable field, and the keyboard is unlocked.

        Sometimes the server will "unlock" the keyboard but the screen will
        not yet be ready.  In that case, an attempt to read or write to the
        screen will result in a 'E' keyboard status because we tried to
        read from a screen that is not yet ready.

        Using this method tells the client to wait until a field is
        detected and the cursor has been positioned on it.
        """
        self.exec_command("Wait({0}, InputField)".format(self.timeout).encode("utf-8"))
        if self.status.keyboard != b"U":
            raise KeyboardStateError(
                "keyboard not unlocked, state was: {0}".format(self.status.keyboard.decode("utf-8"))
            )

    def move_to(self, ypos, xpos):
        """
        move the cursor to the given coordinates.  Coordinates are 1
        based, as listed in the status area of the terminal.
        """
        self.check_limits(ypos, xpos)
        # the screen's coordinates are 1 based, but the command is 0 based
        xpos -= 1
        ypos -= 1
        self.exec_command("MoveCursor({0}, {1})".format(ypos, xpos).encode("utf-8"))

    def send_string(self, tosend, ypos=None, xpos=None):
        """
        Send a string to the screen at the current cursor location or at
        screen coordinates `ypos`/`xpos` if they are both given.

        Coordinates are 1 based, as listed in the status area of the
        terminal.
        """
        if xpos and ypos:
            self.move_to(ypos, xpos)
        # escape double quotes in the data to send
        tosend = tosend.decode("utf-8").replace('"', '"')
        self.exec_command('String("{0}")'.format(tosend).encode("utf-8"))

    def send_enter(self):
        self.exec_command(b"Enter")

    def string_get(self, ypos, xpos, length):
        """
        Get a string of `length` at screen coordinates `ypos`/`xpos`

        Coordinates are 1 based, as listed in the status area of the
        terminal.
        """
        self.check_limits(ypos, xpos)
        if (xpos + length) > (self.model_dimensions["columns"] + 1):
            raise Exception("You have exceeded the x-axis limit of the mainframe screen")
        # the screen's coordinates are 1 based, but the command is 0 based
        xpos -= 1
        ypos -= 1
        cmd = self.exec_command("ascii({0},{1},{2})".format(ypos, xpos, length).encode("utf-8"))
        # this usage of utf-8 should only return a single line of data
        assert len(cmd.data) == 1, cmd.data
        return cmd.data[0].decode("unicode_escape")

    def search_string(self, string, ignore_case=False):
        """
        Check if a string exists on the mainframe screen and return True or False.
        """
        for ypos in range(self.model_dimensions["rows"]):
            line = self.string_get(ypos + 1, 1, self.model_dimensions["columns"])
            if ignore_case:
                string = string.lower()
                line = line.lower()
            if string in line:
                return True
        return False

    def get_string_positions(self, string, ignore_case=False):
        """Returns a list of tuples of ypos and xpos for the position where the `string` was found,
        or an empty list if it was not found."""
        screen_content = self.read_all_screen()
        indices_object = re.finditer(re.escape(string), screen_content, flags=0 if not ignore_case else re.IGNORECASE)
        indices = [index.start() for index in indices_object]
        # ypos and xpos should be returned 1-based
        return [self._get_ypos_and_xpos_from_index(index + 1) for index in indices]

    def read_all_screen(self):
        """
        Read all the mainframe screen and return it in a single string.
        """
        full_text = ""
        for ypos in range(self.model_dimensions["rows"]):
            full_text += self.string_get(ypos + 1, 1, self.model_dimensions["columns"])
        return full_text

    def delete_field(self):
        """
        Delete contents in field at current cursor location and positions
        cursor at beginning of field.
        """
        self.exec_command(b"DeleteField")

    def fill_field(self, ypos, xpos, tosend, length):
        """
        clears the field at the position given and inserts the string
        `tosend`

        tosend: the string to insert
        length: the length of the field

        Coordinates are 1 based, as listed in the status area of the
        terminal.

        raises: FieldTruncateError if `tosend` is longer than
            `length`.
        """
        if length - len(tosend) < 0:
            raise FieldTruncateError('length limit %d, but got "%s"' % (length, tosend))
        if xpos is not None and ypos is not None:
            self.move_to(ypos, xpos)
        self.delete_field()
        self.send_string(tosend)

    def save_screen(self, file_path):
        self.exec_command("PrintText(html,file,{0})".format(file_path).encode("utf-8"))

    def get_current_position(self):
        """Returns the current cursor position as a tuple of 1 indexed integers."""
        command = self.exec_command(b"Query(Cursor)")
        if len(command.data) != 1:
            raise Exception(f'Cursor position returned an unexpected value: "{command.data}"')
        list_of_strings = command.data[0].decode("utf-8").split(" ")
        return tuple([int(i) + 1 for i in list_of_strings])

    def check_limits(self, ypos, xpos):
        if ypos > self.model_dimensions["rows"]:
            raise Exception("You have exceeded the y-axis limit of the mainframe screen")
        if xpos > self.model_dimensions["columns"]:
            raise Exception("You have exceeded the x-axis limit of the mainframe screen")

    def _get_ypos_and_xpos_from_index(self, index):
        ypos = math.ceil(index / self.model_dimensions["columns"])
        remainder = index % self.model_dimensions["columns"]
        if remainder == 0:
            xpos = self.model_dimensions["columns"]
        else:
            xpos = remainder
        return (ypos, xpos)
