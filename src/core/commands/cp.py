import os
import shutil
from src.infrastructure.logger import logger
from src.services.path_normalizer import Normalizer
from src.services.help_call import Helper
from src.services.parameter_validator import ParameterValidator
from src.services.command_logger import CommandLogger


class Cp:
    '''
    Command "cp" takes lists of flags (--help, --recursive or -r) and parameters (>=1 file|folder for copy, 1 target folder).
    If given paths are valid, it copy files.
    Otherwise it returns an exception.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper, validator: ParameterValidator, command_logger: CommandLogger) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._validator = validator
        self._command_logger = command_logger
        self._logger = logger

    def cp(self, long_flags: list[str], parameters: list[str]) -> str:
        self._command_logger.log_command_call("cp", long_flags, parameters)

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("cp")

        # validate parameters
        self._validator.validate_no_parameters(parameters, "cp")
        self._validator.validate_not_enough_parameters(parameters, 2, "cp")

        # processing flags
        recursive = 'recursive' in long_flags

        # target folder processing
        original_folder_path, folder_path = self._normalize.normalize(
            parameters[-1])
        if not os.path.isdir(folder_path):
            self._logger.error(f"Incorrect folder path {folder_path}.")
            raise SyntaxError(
                f"cp: folder path {original_folder_path} is incorrect!")

        # processing copy of files and folders
        output = []
        for file_path in parameters[:-1]:
            original_file_path, file_path = self._normalize.normalize(
                file_path)

            # file was given
            if os.path.isfile(file_path):
                try:
                    # copy file to a directory
                    shutil.copyfile(file_path, os.path.join(
                        folder_path, os.path.basename(file_path)))
                    self._logger.debug(
                        f"Copied file {file_path} to {folder_path}.")
                    output.append(
                        f"Copied file {original_file_path} to {original_folder_path}.")
                except Exception as e:
                    self._logger.exception(f"Failed to copy {file_path}: {e}")
                    output.append(f"cp: failed to copy {original_file_path}.")

            # folder was given
            elif os.path.isdir(file_path):
                # check for recursive flag
                if not recursive:
                    self._logger.warning(
                        f"Failed to copy folder {file_path}. Flag --recursive was not given.")
                    output.append(
                        f"cp: you can't copy folder {original_file_path} without flag [-r|--recursive].")
                else:
                    try:
                        # copy file to a directory
                        shutil.copytree(file_path, os.path.join(
                            folder_path, os.path.basename(file_path)), dirs_exist_ok=True)
                        self._logger.debug(
                            f"Copied folder {file_path} to {folder_path}.")
                        output.append(
                            f"Copied folder {original_file_path} to {original_folder_path}.")
                    # catch unexpected copying exceptions
                    except Exception as e:
                        self._logger.exception(
                            f"Failed to copy {file_path}: {e}")
                        output.append(
                            f"cp: failed to copy {original_file_path}.")

            # invalid file was given
            else:
                self._logger.error(f"Path not found: {file_path}")
                output.append(
                    f"cp: failed to copy {original_file_path}. It doesn't exist.")

        self._logger.info("Cp successfully copied all valid files.")
        return "\n".join(output)


COMMAND_INFO = {
    "name": "cp",
    "function": lambda: Cp(Normalizer(), Helper(), ParameterValidator(), CommandLogger()),
    "entry-point": "cp",
    "flags": ["recursive", "help"],
    "aliases": {"r": "recursive"},
    "description": "Copy files to a different folder."
}
