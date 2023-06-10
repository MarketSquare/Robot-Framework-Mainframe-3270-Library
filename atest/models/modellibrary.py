from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


built_in = BuiltIn()
try:
    library = built_in.get_library_instance("Mainframe3270")
except RobotNotRunningError:
    pass


def emulator_model_should_be(model):
    error_message = f'Emulator model should have been "{model}", but was "{library.mf.model}"'
    built_in.should_be_equal_as_strings(model, library.mf.model, error_message, False)
