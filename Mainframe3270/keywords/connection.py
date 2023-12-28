import os
import re
import shlex
from os import name as os_name
from typing import List, Optional, Union
from robot.api import logger
from robot.api.deco import keyword
from Mainframe3270.librarycomponent import LibraryComponent
from Mainframe3270.py3270 import Emulator


class ConnectionKeywords(LibraryComponent):
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
        To establish a connection, only the hostname is required.
        Optional parameters include logical unit name (LU) and port.

        Additional configuration data can be provided through the `extra_args` parameter.
        `extra_args` accepts either a list or a path
        to a file containing [https://x3270.miraheze.org/wiki/Category:Command-line_options|x3270 command line options].

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
        Refer to the [https://x3270.miraheze.org/wiki/Wc3270/Command-line_options|wc3270 command line options]
        for a subset of available options.

        Note: If you specify the port with the `-port` command-line option in `extra_args`
        (or use the -xrm resource command for it), it will take precedence over the `port` argument provided
        in the `Open Connection` keyword.

        This keyword returns the index of the opened connection, which can be used to reference the connection
        when switching between connections using the `Switch Connection` keyword. For more information on opening
        and switching between multiple connections, please refer to the `Concurrent Connections` section.

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

    @staticmethod
    def _process_args(args) -> list:
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

    @staticmethod
    def _get_model_from_list_or_file(list_or_file):
        pattern = re.compile(r"[wcxs3270.*]+model:\s*([327892345E-]+)")
        match = None
        if isinstance(list_or_file, list):
            match = pattern.findall(str(list_or_file))
        elif isinstance(list_or_file, os.PathLike) or isinstance(list_or_file, str):
            with open(list_or_file) as file:
                match = pattern.findall(file.read())
        return None if not match else match[-1]

    @staticmethod
    def _port_in_extra_args(args) -> bool:
        if not args:
            return False
        pattern = re.compile(r"[wcxs3270.*-]+port[:]{0,1}")
        if pattern.search(str(args)):
            return True
        return False

    @keyword("Open Connection From Session File")
    def open_connection_from_session_file(self, session_file: os.PathLike, alias: Optional[str] = None) -> int:
        """Create a connection to an IBM3270 mainframe
        using a [https://x3270.miraheze.org/wiki/Session_file|session file].

        The session file contains [https://x3270.miraheze.org/wiki/Category:Resources|resources (settings)]
        for a specific host session.

        The only mandatory setting required to establish the connection
        is the [https://x3270.miraheze.org/wiki/Hostname_resource|hostname resource].

        This keyword is an alternative to `Open Connection`. Please note that the Robot-Framework-Mainframe-3270-Library
        currently only supports model "2". Specifying any other model will result in a failure.

        For more information on session file syntax and detailed examples, please
        consult the [https://x3270.miraheze.org/wiki/Session_file|x3270 wiki].

        This keyword returns the index of the opened connection, which can be used to reference the connection
        when switching between connections using the `Switch Connection` keyword. For more information on opening and
        switching between multiple connections, please refer to the `Concurrent Connections` section.

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

    @staticmethod
    def _check_contains_hostname(session_file):
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
        """Switch the current connection to the one identified by index or alias. Indices are returned from
        and aliases can be optionally provided to the `Open Connection` and `Open Connection From Session File`
        keywords.

        For more information on opening and switching between multiple connections,
        please refer to the `Concurrent Connections` section.

        Examples:
        | Open Connection | Hostname | alias=first |
        | Open Connection | Hostname | alias=second | # second is now the current connection |
        | Switch Connection | first | | # first is now the current connection  |
        """
        self.cache.switch(alias_or_index)

    @keyword("Close Connection")
    def close_connection(self) -> None:
        """
        Close the current connection.
        """
        self.mf.terminate()

    @keyword("Close All Connections")
    def close_all_connections(self) -> None:
        """
        Close all currently opened connections and reset the index counter to 1.
        """
        self.cache.close_all("terminate")
