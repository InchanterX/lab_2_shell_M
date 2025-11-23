import os
import shutil
from src.infrastructure.logger import logger
from src.services.path_normalizer import Normalizer
from src.services.help_call import Helper


class Mv:
    '''
    Command "mv" move files to the specified place.
    If only two files were given and they are adjacent in their positioning - file will be just replaced.
    If more files were given and everything is valid they will be moved to a given folder.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logger

    def mv(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running mv with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("mv")

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("mv: No parameters were given.")

        # not enough parameters were given
        if len(parameters) == 1:
            self._logger.error("Not enough parameters were given.")
            raise SyntaxError("mv: Not enough parameters were given.")

        # rename mode
        original_folder_path, folder_path = self._normalize.normalize(
            parameters[-1])
        if len(parameters) == 2 and not os.path.isdir(folder_path):
            return self._rename(parameters[0], parameters[1])

        if not os.path.isdir(folder_path):
            self._logger.error(f"Target folder {folder_path} is invalid")
            raise SyntaxError(f"mv: target {original_folder_path} is invalid!")

        output = self._move(parameters[:-1], folder_path)
        return "\n".join(output)

    def _rename(self, primary_file: str, new_file: str) -> str:
        '''
        Function that renames files.
        Used for cases when two files were given and there is no other parameters.
        Get original file and move it to the new place with a new name.
        '''
        output = []
        original_primary_file, primary_file = self._normalize.normalize(
            primary_file)
        original_new_file, new_file = self._normalize.normalize(
            new_file)

        # check for paths visibility
        if not os.path.exists(primary_file):
            self._logger.error(f"Path {primary_file} is invalid.")
            output.append(f"mv: {original_primary_file} doesn't exist!")
            return "\n".join(output)

        # moving
        shutil.move(primary_file, new_file)
        self._logger.info(f"Renamed {primary_file} to {new_file}")
        return "\n".join(output)

    def _move(self, files: list[str], folder: str) -> list:
        '''
        Move all files that were given in the parameters to a folder.
        Get list of paths to move and target folder. Returns list of errors if they occurred.
        '''
        output = []
        for file in files:
            original_file, file = self._normalize.normalize(file)
            if not os.path.exists(file):
                self._logger.error(f"{file} does't exist!")
                output.append(f"mv: {original_file} doesn't exist!")
                continue

            shutil.move(file, folder)
            self._logger.info(f"Moved {file} to {folder}.")
        return output


COMMAND_INFO = {
    "name": "mv",
    "function": lambda: Mv(Normalizer(), Helper()),
    "entry-point": "mv",
    "flags": ["help"],
    "aliases": {},
    "description": "Display file content."
}
