from Mainframe3270 import Mainframe3270
from Mainframe3270.py3270 import Emulator


def create_test_object_for(library_component):
    """Creates a test object for a keyword class that inherits from Mainframe3270.librarycomponent.LibraryComponent.
    It also registers a Mainframe3270.py3270.Emulator instance so that the test run without raising a RuntimeError.

    Example:
    >>> import pytest
    >>> from Mainframe3270.keywords import AssertionKeywords

    >>> @pytest.fixture
    >>> def under_test():
    >>>     return create_test_object_for(AssertionKeywords)
    """
    under_test = library_component(Mainframe3270())
    under_test.cache.register(Emulator(), None)
    return under_test
