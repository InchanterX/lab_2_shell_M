from src.infrastructure.logger import logger
import src.infrastructure.constants as constants
from src.services.path_normalizer import Normalizer
from src.services.help_call import Helper
from src.services.command_logger import CommandLogger
import os


class Cd:
    '''
    Command "cd" changes current directory.
    It get flags and parameters and change the constant variable CURRENT_PATH.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper, command_logger: CommandLogger) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._command_logger = command_logger
        self._logger = logger

    def cd(self, long_flags: list[str], parameters: list[str]) -> str:
        self._command_logger.log_command_call("cd", long_flags, parameters)

        # call help
        if 'help' in long_flags:
            return self._helper.call_help("cd")

        # if parameters are empty switch to user's home folder
        if parameters == []:
            constants.CURRENT_DIR = constants.USER_HOME_DIR

        output = []
        # otherwise it process given parameters. Yes it can switch folders several times. Why not?
        for parameter in parameters:
            # converting parameter to an absolute normalized path
            original_parameter, parameter = self._normalize.normalize(
                parameter)

            # raise a error if file is given
            if os.path.isfile(parameter):
                self._logger.exception(
                    f"Command can't switch to {parameter}. It's a file!")
                output.append(
                    f"cd: You can't switch to {original_parameter}. It's a file!")
            # change directory if everything is right
            elif os.path.isdir(parameter):
                constants.CURRENT_DIR = parameter
            # raise a error if path is incorrect
            else:
                self._logger.exception(
                    f"Path {parameter} doesn't exist.")
                output.append(f"cd: Path {original_parameter} doesn't exist!")
        return "\n".join(output)


COMMAND_INFO = {
    "name": "cd",
    "function": lambda: Cd(Normalizer(), Helper(), CommandLogger()),
    "entry-point": "cd",
    "flags": ["help"],
    "aliases": {},
    "description": "Give an ability to switch between folders."
}
