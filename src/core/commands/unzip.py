import os
import zipfile
from src.infrastructure.logger import logger
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer
from src.services.parameter_validator import ParameterValidator
from src.services.command_logger import CommandLogger


class Unzip:
    '''
    "Unzip" unzips zip archives.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper, validator: ParameterValidator, command_logger: CommandLogger) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._validator = validator
        self._command_logger = command_logger
        self._logger = logger

    def unzip(self, long_flags: list[str], parameters: list[str]) -> str:
        self._command_logger.log_command_call("unzip", long_flags, parameters)

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("unzip")

        # validate parameters
        self._validator.validate_no_parameters(parameters, "unzip")

        # processing parameters
        output = []
        for parameter in parameters:
            original_path, path = self._normalize.normalize(
                parameter)
            if not os.path.exists(path):
                self._logger.error(f"Path {path} is invalid.")
                output.append(f"unzip: {original_path} doesn't exist!")
            elif not os.access(path, os.R_OK):
                self._logger.error(f"Path {path} is unaccessible.")
                output.append(f"unzip: Can't access {original_path}!")
            elif not zipfile.is_zipfile(path):
                self._logger.error(
                    f"{path} can't be unzipped because it isn't an archive.")
                output.append(
                    f"unzip: Can't unzip {original_path}. It isn't an archive!")
            else:
                target_directory = os.path.dirname(path)
                try:
                    with zipfile.ZipFile(path, "r") as my_zip:
                        my_zip.extractall(target_directory)
                        self._logger.info(
                            f"Successfully unzipped file {path}.")
                        output.append(
                            f"Successfully unzipped file {original_path}.")
                except OSError:
                    self._logger.exception(f"Unable to unzip {path}.")
                    output.append(f"Unable to unzip {original_path}!")

        return '\n'.join(output)


COMMAND_INFO = {
    "name": "unzip",
    "function": lambda: Unzip(Normalizer(), Helper(), ParameterValidator(), CommandLogger()),
    "entry-point": "unzip",
    "flags": ["help"],
    "aliases": {},
    "description": "Unzip zip archives."
}
