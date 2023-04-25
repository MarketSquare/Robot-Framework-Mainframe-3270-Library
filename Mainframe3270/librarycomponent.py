from datetime import timedelta

from robot.utils import ConnectionCache

from Mainframe3270.py3270 import Emulator


class LibraryComponent:
    """
    This is the base class to be inherited by the keyword classes under Mainframe3270/keywords.
    It is a helper class that makes attributes from the Mainframe3270 class available to the keyword classes.
    """

    def __init__(self, library):
        """
        :param library: The Robot-Framework-Mainframe-3270-Library itself.
        :type library: Mainframe3270.Mainframe3270
        """
        self.library = library

    @property
    def visible(self) -> bool:
        return self.library.visible

    @visible.setter
    def visible(self, value: bool):
        self.library.visible = value

    @property
    def timeout(self) -> timedelta:
        return self.library.timeout

    @property
    def wait_time(self) -> timedelta:
        return self.library.wait_time

    @property
    def wait_time_after_write(self) -> timedelta:
        return self.library.wait_time_after_write

    @property
    def img_folder(self) -> str:
        return self.library.img_folder

    @property
    def cache(self) -> ConnectionCache:
        return self.library.cache

    @property
    def mf(self) -> Emulator:
        return self.library.cache.current
