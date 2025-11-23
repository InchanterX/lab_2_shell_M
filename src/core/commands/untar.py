import os
import tarfile
from src.infrastructure.logger import logger
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer
from src.services.parameter_validator import ParameterValidator
from src.services.command_logger import CommandLogger


class Untar:
    '''
    "Untar" tar.gz archives.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper, validator: ParameterValidator, command_logger: CommandLogger) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._validator = validator
        self._command_logger = command_logger
        self._logger = logger

    def untar(self, long_flags: list[str], parameters: list[str]) -> str:
        self._command_logger.log_command_call("untar", long_flags, parameters)

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("untar")

        # validate parameters
        self._validator.validate_no_parameters(parameters, "untar")

        # processing parameters
        output = []
        for parameter in parameters:
            original_path, path = self._normalize.normalize(
                parameter)
            if not os.path.exists(path):
                self._logger.error(f"Path {path} is invalid.")
                output.append(f"untar: {original_path} doesn't exist!")
            elif not os.access(path, os.R_OK):
                self._logger.error(f"Path {path} is unaccessible.")
                output.append(f"untar: Can't access {original_path}!")
            elif not tarfile.is_tarfile(path):
                self._logger.error(
                    f"{path} can't be untarred because it isn't an archive.")
                output.append(
                    f"untar: Can't untar {original_path}. It isn't an archive!")
            else:
                target_directory = os.path.dirname(path)
                try:
                    with tarfile.open(path, "r:*") as my_tar:
                        my_tar.extractall(target_directory)
                        self._logger.info(
                            f"Successfully untarred file {path}.")
                        output.append(
                            f"Successfully untarred file {original_path}.")
                except OSError:
                    self._logger.exception(f"Unable to untar {path}.")
                    output.append(f"Unable to untar {original_path}!")

        return '\n'.join(output)


COMMAND_INFO = {
    "name": "untar",
    "function": lambda: Untar(Normalizer(), Helper(), ParameterValidator(), CommandLogger()),
    "entry-point": "untar",
    "flags": ["help"],
    "aliases": {},
    "description": "Untar zip archives."
}
