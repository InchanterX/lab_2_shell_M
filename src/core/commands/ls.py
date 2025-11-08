import os
import stat
import datetime
import src.infrastructure.constants as constants
import logging
from src.services.path_normalizer import Normalizer
from src.services.help_call import Helper


class Ls:
    '''
    Command "ls" get parameters and flags and return lists of files in the directories from the parameters.
    It takes unlimited amount of parameters with paths and return their files independently.
    Command supports flags "all", "long" and "help". "All" shows all the files in the folder, even hidden (with dot).
    "Long" extend information about every file and information. "Help" return help.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logging.getLogger(__name__)

    def ls(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running ls with flags={long_flags}, parameters={parameters}")

        # return help if such flag is given
        if 'help' in long_flags:
            return self._helper.call_help("ls")

        results = []
        output = []
        dirs = []

        # if no parameters are given, works with current directory
        if parameters == []:
            results.append(os.listdir(constants.CURRENT_DIR))
            parameters.append(constants.CURRENT_DIR)
            dirs.append(constants.CURRENT_DIR)
            self._logger.debug("No parameters were given, using CURRENT_DIR")
        # otherwise process every parameter by an algorithm
        else:
            for parameter in parameters:
                original_parameter, parameter = self._normalize.normalize(
                    parameter)
                try:
                    # if file is given, append error and continue
                    if os.path.isfile(parameter):
                        self._logger.warning(
                            f"Failed to list {parameter}. It's a file.")
                        output.append(
                            f"ls: {original_parameter} can't be listed. It's a file!")
                    # if directory is given, append row list of files in it
                    elif os.path.isdir(parameter):
                        results.append(os.listdir(parameter))
                        dirs.append(parameter)
                        self._logger.debug(
                            f"Listed directory {parameter}")
                    # otherwise append a error to the output, b/c path is invalid
                    else:
                        self._logger.error(
                            f"Invalid path {original_parameter}.")
                        output.append(
                            f"ls: Path {original_parameter} is invalid!")
                # if program failed to process file it is unaccessible
                except PermissionError:
                    self._logger.exception(
                        f"There is no permissions to delete {parameter}.")
                    output.append(
                        f"ls: cannot delete {original_parameter}. Permission denied.")

        # process flag --all if it was given
        if 'all' not in long_flags:
            for r in range(len(results)):
                results[r] = [file for file in results[r]
                              if not file.startswith('.')]

        # process flag --long and extend file information with permissions, hard links, size and last modification date
        # If there will be enough time it will be great to add owners, groups and lining for output
        final_output = []
        if 'long' in long_flags:
            for r in range(len(results)):
                for file in results[r]:
                    file_stat = os.stat(os.path.join(dirs[r], file))
                    file_permissions = stat.filemode(file_stat.st_mode)
                    file_links = file_stat.st_nlink
                    file_size = file_stat.st_size
                    file_modified = datetime.datetime.fromtimestamp(
                        file_stat.st_mtime).strftime("%b %d %H:%M")
                    file_data = f"{file_permissions}  {file_links}  {file_size}  {file_modified} {file}"
                    final_output.append(file_data)
            final_output = output + final_output
            return "\n".join(final_output)
        # otherwise just split the output with spaces
        else:
            for result in results:
                final_output.extend(result)
            final_output = output + final_output
            return "   ".join(final_output)


COMMAND_INFO = {
    "name": "ls",
    "function": lambda: Ls(Normalizer(), Helper()),
    "entry-point": "ls",
    "flags": ["all", "long", "help"],
    "aliases": {"a": "all", "l": "long"},
    "description": "List files in the given folder."


}
