import os
import stat
import datetime
import src.utils.constants as constants
import logging


class Ls:
    '''
    Command "list"
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def ls(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running ls with flags={long_flags}, parameters={parameters}")
        if 'help' in long_flags:
            return 'ls lists folders'
        results = []
        output = []
        dirs = []
        if parameters == []:
            results.append(os.listdir(constants.CURRENT_DIR))
            parameters.append(constants.CURRENT_DIR)
            dirs.append(constants.CURRENT_DIR)
            self._logger.info("No parameters were given, using CURRENT_DIR")
        else:
            for parameter in parameters:
                original_parameter = parameter
                parameter = parameter.replace('\'', '')
                print(parameter)
                parameter = os.path.expanduser(parameter)
                if not os.path.isabs(parameter):
                    parameter = os.path.join(constants.CURRENT_DIR, parameter)
                parameter = os.path.normpath(parameter)
                self._logger.debug(
                    f"Converted parameters: {original_parameter} -> {parameter}")
                try:
                    if os.path.isfile(parameter):
                        self._logger.warning(
                            f"Failed to list {parameter}. It's a file.")
                        output.append(
                            f"ls: {original_parameter} can't be listed. It's a file!")
                    elif os.path.isdir(parameter):
                        results.append(os.listdir(parameter))
                        dirs.append(parameter)
                        self._logger.debug(
                            f"Listed directory {parameter}")
                    else:
                        self._logger.error(
                            f"Invalid path {original_parameter}.")
                        output.append(
                            f"ls: Path {original_parameter} is invalid!")
                except OSError as e:
                    self._logger.exception(
                        f"Failed to access {parameter}: {e}")
                    output.append(f"ls: cannot access {original_parameter}!")

        if 'all' not in long_flags:
            for r in range(len(results)):
                results[r] = [file for file in results[r]
                              if not file.startswith('.')]

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
        else:
            for result in results:
                final_output.extend(result)
            final_output = output + final_output
            return "   ".join(final_output)


COMMAND_INFO = {
    "name": "ls",
    "function": Ls,
    "entry-point": "ls",
    "flags": ["all", "long", "help"],
    "aliases": {"a": "all", "l": "long"},
    "description": "List files in the given folder."


}
