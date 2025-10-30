import src.utils.constants as constants
from src.utils.path_normalizer import Normalizer
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
            # Converting parameter to an absolute normalized path
            original_parameter = parameter
            parameter = Normalizer().normalize(parameter)
            # parameter = os.path.expanduser(parameter)
            # if not os.path.isabs(parameter):
            #     parameter = os.path.join(constants.CURRENT_DIR, parameter)
            # parameter = os.path.normpath(parameter)

            if os.path.isfile(parameter):
                raise SyntaxError(
                    f"cd: You can't switch to {original_parameter}. It's a file!")
            elif os.path.isdir(parameter):
                constants.CURRENT_DIR = parameter
            else:
                raise SyntaxError(
                    f"cd: Path {original_parameter} doesn't exist!")
        return ""


COMMAND_INFO = {
    "name": "cd",
    "function": Cd,
    "entry-point": "cd",
    "flags": ["help"],
    "aliases": {},
    "description": "Give an ability to switch between folders."
}
