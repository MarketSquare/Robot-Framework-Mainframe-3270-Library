import os
from pathlib import Path
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
    assert library.model == under_test.model


def test_can_set_visible():
    library = Mainframe3270(visible=True)
    under_test = LibraryComponent(library)

    assert library.visible == under_test.visible is True

    under_test.visible = False

    assert library.visible == under_test.visible is False


def test_can_set_timeout():
    library = Mainframe3270(timeout="1 minute")
    under_test = LibraryComponent(library)

    assert library.timeout == under_test.timeout == 60.0

    under_test.timeout = 10.0

    assert library.timeout == under_test.timeout == 10.0


def test_can_set_wait_time():
    library = Mainframe3270(wait_time="5 seconds")
    under_test = LibraryComponent(library)

    assert library.wait_time == under_test.wait_time == 5.0

    under_test.wait_time = 1.0

    assert library.wait_time == under_test.wait_time == 1.0


def test_can_set_wait_time_after_write():
    library = Mainframe3270(wait_time_after_write="5 seconds")
    under_test = LibraryComponent(library)

    assert library.wait_time_after_write == under_test.wait_time_after_write == 5.0

    under_test.wait_time_after_write = 0.5

    assert library.wait_time_after_write == under_test.wait_time_after_write == 0.5


def test_can_set_img_folder(mocker):
    initial_path = Path(os.getcwd()) / "my_initial_folder"
    initial_path_str = str(initial_path)
    new_path = Path(os.getcwd()) / "another_folder"
    new_path_str = str(new_path)
    mock_library = mocker.MagicMock()
    mock_library.img_folder = initial_path_str
    under_test = LibraryComponent(mock_library)

    assert mock_library.img_folder == under_test.img_folder == initial_path_str

    under_test.img_folder = new_path_str

    assert mock_library.img_folder == under_test.img_folder == new_path_str
