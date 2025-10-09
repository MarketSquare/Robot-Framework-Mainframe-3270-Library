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
    def timeout(self):
        return self.library.timeout

    @timeout.setter
    def timeout(self, value):
        self.library.timeout = value

    @property
    def wait_time(self):
        return self.library.wait_time

    @wait_time.setter
    def wait_time(self, value):
        self.library.wait_time = value

    @property
    def wait_time_after_write(self):
        return self.library.wait_time_after_write

    @wait_time_after_write.setter
    def wait_time_after_write(self, value):
        self.library.wait_time_after_write = value

    @property
    def img_folder(self):
        return self.library.img_folder

    @img_folder.setter
    def img_folder(self, value):
        self.library.img_folder = value

    @property
    def cache(self) -> ConnectionCache:
        return self.library.cache

    @property
    def mf(self) -> Emulator:
        return self.library.cache.current

    @property
    def output_folder(self):
        return self.library.output_folder

    @property
    def model(self):
        return self.library.model
