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

    def emulator_model_should_be(self, model):
        error_message = f'Emulator model should have been "{model}", but was "{self.library.mf.model}"'
        self.built_in.should_be_equal_as_strings(model, self.library.mf.model, error_message, False)

    def _end_keyword(self, name, attributes):
        if attributes["kwname"] in [
            "Open Connection",
            "Open Connection From Session File",
            "Close Connection",
            "Close All Connections",
        ]:
            time.sleep(1.5)
