import os
import shutil
import logging
import src.utils.constants as constants
from src.utils.path_normalizer import Normalizer


class Cp:
    '''
    Command "cp" takes lists of flags and parameters.
    If given paths to 1 or more files and a folder to copy in, it copy files.
    Otherwise it return an exception.
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def cp(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running cp with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return 'cp [-r|--recursive|--help] [file1 ... fileN folder] - display file\'s content.'

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("cp: No parameters were given.")

        # no enough parameters were given
        if len(parameters) == 1:
            self._logger.error("Not enough parameters were given.")
            raise SyntaxError("cp: Not enough parameters were given.")

        # processing parameters
        if 'recursive' in long_flags:
            recursive = 1
        else:
            recursive = 0

        # target folder processing
        original_folder_path = parameters[-1]
        folder_path = Normalizer().normalize(parameters[-1])
        if not os.path.isdir(folder_path):
            self._logger.error(f"Incorrect folder path {folder_path}.")
            raise SyntaxError(
                f"cp: folder path {original_folder_path} is incorrect!")

        # processing copy of files and folders
        output = []
        for file_path in parameters[:-1]:
            original_file_path = file_path
            file_path = Normalizer().normalize(file_path)

            # file given
            if os.path.isfile(file_path):
                try:
                    shutil.copyfile(file_path, os.path.join(
                        folder_path, os.path.basename(file_path)))
                    self._logger.debug(
                        f"Copied file {file_path} to {folder_path}.")
                except Exception as e:
                    self._logger.exception(f"Failed to copy {file_path}: {e}")
                    output.append(f"cp: failed to copy {original_file_path}.")

            # folder given
            elif os.path.isdir(file_path):
                if recursive == 0:
                    self._logger.warning(
                        f"Failed to copy folder {file_path}. Flag --recursive was not given.")
                    output.append(
                        f"cp: you can't copy folder {original_file_path} without flag [-r|--recursive].")
                else:
                    try:
                        shutil.copytree(file_path, os.path.join(
                            folder_path, os.path.basename(file_path)), dirs_exist_ok=True)
                        self._logger.debug(
                            f"Copied folder {file_path} to {folder_path}.")
                    except Exception as e:
                        self._logger.exception(
                            f"Failed to copy {file_path}: {e}")
                        output.append(
                            f"cp: failed to copy {original_file_path}.")

            # invalid file given
            else:
                self._logger.error(f"Path not found: {file_path}")
                output.append(
                    f"cp: failed to copy {original_file_path}. It doesn't exist.")

        return "\n".join(output)


COMMAND_INFO = {
    "name": "cp",
    "function": Cp,
    "entry-point": "cp",
    "flags": ["recursive", "help"],
    "aliases": {"r": "recursive"},
    "description": "Copy files to a different folder."
}
