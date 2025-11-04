import os
import logging
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer


class Cat:
    '''
    Command "cat" takes lists of flags and parameters.
    If given paths in parameters are valid, command displays their content.
    Otherwise it return corresponding error.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logging.getLogger(__name__)

    def cat(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running cat with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("cat")

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("cat: No parameters were given.")

        # processing all given parameters
        output = []
        for parameter in parameters:
            # Converting parameter to a absolute normalized path
            original_parameter, parameter = self._normalize.normalize(
                parameter)

            try:
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

            except OSError as e:
                self._logger.exception(
                    f"Failed to access {parameter}: {e}")
                output.append(f"cat: cannot access {original_parameter}!")

        return "\n".join(output)


COMMAND_INFO = {
    "name": "cat",
    "function": Cat,
    "entry-point": "cat",
    "flags": ["help"],
    "aliases": {},
    "description": "Display file content."
}
