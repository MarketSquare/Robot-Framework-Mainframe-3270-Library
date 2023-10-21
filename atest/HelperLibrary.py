import os
import time

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class HelperLibrary:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.built_in = BuiltIn()
        self.ROBOT_LIBRARY_LISTENER = self
        try:
            self.library = self.built_in.get_library_instance("Mainframe3270")
        except RobotNotRunningError:
            pass

    def create_session_file(self, *content_lines):
        extensions = {
            ("nt", True): "wc3270",
            ("nt", False): "ws3270",
            ("posix", True): "x3270",
            ("posix", False): "s3270",
        }
        extension = extensions.get((os.name, self.library.visible))
        session_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", f"session.{extension}")
        with open(session_file, "w", encoding="utf-8") as file:
            for line in content_lines:
                file.write(line + "\n")
        return session_file

    def emulator_model_should_be(self, model):
        error_message = f'Emulator model should have been "{model}", but was "{self.library.mf.model}"'
        self.built_in.should_be_equal_as_strings(model, self.library.mf.model, error_message, False)

    def move_cursor_to(self, ypos, xpos):
        self.library.mf.move_to(int(ypos), int(xpos))

    def _end_keyword(self, name, attributes):
        if attributes["kwname"] in [
            "Open Connection",
            "Open Connection From Session File",
            "Close Connection",
            "Close All Connections",
        ]:
            time.sleep(1.5)
