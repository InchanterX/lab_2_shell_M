import os
from src.infrastructure.logger import logger
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer
from src.services.parameter_validator import ParameterValidator
from src.services.command_logger import CommandLogger


class Cat:
    '''
    Command "cat" takes lists of flags and parameters.
    If given paths in parameters are valid, command displays their content.
    Otherwise it returns corresponding error.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper, validator: ParameterValidator, command_logger: CommandLogger) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._validator = validator
        self._command_logger = command_logger
        self._logger = logger

    def cat(self, long_flags: list[str], parameters: list[str]) -> str:
        self._command_logger.log_command_call("cat", long_flags, parameters)

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("cat")

        # validate parameters
        self._validator.validate_no_parameters(parameters, "cat")

        # processing all given parameters
        output = []
        for parameter in parameters:
            # Converting parameter to a absolute normalized path
            original_parameter, parameter = self._normalize.normalize(
                parameter)

            # dir was given
            if os.path.isdir(parameter):
                self._logger.warning(
                    f"Failed to display {parameter}. It's a file.")
                output.append(
                    f"cat: {original_parameter} can't be displayed. It's a directory!")

            # file was given
            elif os.path.isfile(parameter):
                try:
                    with open(parameter, "r", encoding="UTF-8") as file:
                        file_content = file.read()
                        self._logger.debug(
                            f"Successfully opened and displayed file {parameter}.")
                        output.append(file_content)
                # append a error to the output if file is binary
                except UnicodeDecodeError:
                    self._logger.exception(
                        f"File {parameter} can't be displayed. It is binary file.")
                    output.append(
                        f"cat: cannot display binary file {original_parameter}!")
                # append a error to the output if file is unaccessible
                except PermissionError:
                    self._logger.exception(
                        f"Failed to access {parameter}.")
                    output.append(
                        f"cat: cannot access {original_parameter}!")
                continue

            # incorrect path was given
            else:
                self._logger.exception(
                    f"Failed to display {parameter}. Path is incorrect.")
                output.append(
                    f"cat: file {original_parameter} does not exist!")

        return "\n".join(output)


COMMAND_INFO = {
    "name": "cat",
    "function": lambda: Cat(Normalizer(), Helper(), ParameterValidator(), CommandLogger()),
    "entry-point": "cat",
    "flags": ["help"],
    "aliases": {},
    "description": "Display file content."
}
