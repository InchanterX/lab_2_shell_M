import src.utils.constants as constants
from src.utils.path_normalizer import Normalizer
import os
import logging


class Cd:
    '''
    Command "cd" change current directory.
    It get flags and parameters and change the constant variable CURRENT_PATH.
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def cd(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running cd with flags={long_flags}, parameters={parameters}")

        # call help
        if long_flags != [] and long_flags[0] == "help":
            return "cd [parameter] change the current directory"

        # if parameters are empty switch to user's home folder
        if parameters == []:
            constants.CURRENT_DIR = constants.USER_HOME_DIR

        # otherwise it process given parameters. Yes it can switch folders several times. Why not?
        for parameter in parameters:
            # converting parameter to an absolute normalized path
            original_parameter = parameter
            parameter = Normalizer().normalize(parameter)

            # raise a error if file is given
            if os.path.isfile(parameter):
                raise SyntaxError(
                    f"cd: You can't switch to {original_parameter}. It's a file!")
            # change directory if everything is right
            elif os.path.isdir(parameter):
                constants.CURRENT_DIR = parameter
            # raise a error if path is incorrect
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
