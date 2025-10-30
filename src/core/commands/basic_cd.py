import src.utils.constants as constants
import os


class Cd:
    '''
    Command "cd"
    '''

    def __init__(self) -> None:
        pass

    def cd(self, long_flag: list[str], parameters: list[str]) -> str:
        if long_flag != [] and long_flag[0] == "help":
            return "cd"  # should return values from separate module "help" that forms the message depends on the command
        if parameters == []:
            constants.CURRENT_DIR = constants.USER_HOME_DIR

        for parameter in parameters:
            # Converting parameter to a absolute normalized path
            parameter = os.path.expanduser(parameter)
            if not os.path.isabs(parameter):
                parameter = os.path.join(constants.CURRENT_DIR, parameter)
            parameter = os.path.normpath(parameter)

            if os.path.isfile(parameter):
                raise SyntaxError(
                    f"cd: You can't switch to {parameter}. It's a file!")
            elif os.path.isdir(parameter):
                print(parameter)
                constants.CURRENT_DIR = parameter
            else:
                raise SyntaxError(f"cd: Path {parameter} doesn't exist!")
        return ""


COMMAND_INFO = {
    "name": "cd",
    "function": Cd,
    "entry-point": "cd",
    "flags": ["help"],
    "aliases": {},
    "description": "Give an ability to switch between folders."
}
