from Mainframe3270 import Mainframe3270
from Mainframe3270.librarycomponent import LibraryComponent


def test__init__():
    library = Mainframe3270()
    under_test = LibraryComponent(library)

    assert under_test.library == library


def test_librarycomponent_returns_common_attributes():
    library = Mainframe3270()
    under_test = LibraryComponent(library)

    assert library.visible == under_test.visible
    assert library.timeout == under_test.timeout
    assert library.wait_time == under_test.wait_time
    assert library.wait_time_after_write == under_test.wait_time_after_write
    assert library.img_folder == under_test.img_folder
    assert library.cache == under_test.cache
    assert library.mf == under_test.mf


def test_can_set_visible():
    library = Mainframe3270(visible=True)
    under_test = LibraryComponent(library)

    assert library.visible == under_test.visible is True

    under_test.visible = False

    assert library.visible == under_test.visible is False
