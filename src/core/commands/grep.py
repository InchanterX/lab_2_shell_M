from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer
import src.infrastructure.constants as constants
import logging
import re
import os
# import src.utils.constants


class Grep:
    '''
    Command "grep" get regular expression and paths from the command
    and search by this regular expression in following files.
    Supports flag -r for recursive search and -i for registry independent search.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logging.getLogger(__name__)

    def _process_regular_expression(self, regular_expression: str, ignore_case: bool) -> re.Pattern[str]:
        '''
        Get regular expression and use compile on ot for more convenient usage in future.
        If given expression is invalid function will return a error.
        '''
        try:
            if ignore_case:
                prepared_regular_expression = re.compile(
                    regular_expression, flags=re.IGNORECASE)
            else:
                prepared_regular_expression = re.compile(
                    regular_expression)
        except re.error:
            self._logger.exception(
                f"{regular_expression} is invalid and can't be processed.")
            raise SyntaxError(
                f"Pattern {regular_expression} can't be processed. It is invalid.")
        return prepared_regular_expression

    def _process_file(self, path: str, original_path: str, regular_expression: re.Pattern[str]) -> list[str]:
        '''
        Find all the matches in lines of given file
        and return them in numerated list of strings.
        '''
        output = []
        try:
            with open(path, "r", encoding="UTF-8", errors="ignore") as file:
                for order, line in enumerate(file):
                    for match in regular_expression.finditer(line):
                        output.append(
                            f"{file.name} {order+1} {match.group(0).rstrip()}")
        except PermissionError:
            self._logger.error(
                f"Unable to open file {path}. Permission denied.")
            output.append(
                f"grep: cannot search in {original_path}. Permission denied.")
        return output

    def _process_directory(self, path: str, original_path: str, regular_expression: re.Pattern[str]) -> list[str]:
        output = []
        try:
            files = os.listdir(path)
            for file in files:
                try:
                    nested_path = os.path.join(path, file)
                    nested_original_path = os.path.join(original_path, file)
                    if not os.path.exists(nested_path):
                        self._logger.error(
                            f"File {nested_path} doesn't exists.")
                        output.append(
                            f"grep: File {nested_original_path} can't be processed. It doesn't exist.")
                    elif os.path.isfile(nested_path):
                        output += (self._process_file(nested_path,
                                                      nested_original_path, regular_expression))
                    else:
                        output += (self._process_directory(nested_path,
                                                           nested_original_path, regular_expression))
                except PermissionError:
                    self._logger.exception(
                        f"There is no permissions to {nested_path}.")
                    output.append(
                        f"grep: cannot search in {nested_original_path}. Permission denied.")
        except PermissionError:
            self._logger.exception(
                f"There is no permissions to {path}.")
            output.append(
                f"grep: cannot search in {original_path}. Permission denied.")
        return output

    def grep(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running grep with flags={long_flags}, parameters={parameters}")

        # return help if such flag is given
        if 'help' in long_flags:
            return self._helper.call_help("grep")

        # no parameters were given
        if len(parameters) == 0:
            self._logger.error("No parameters were given.")
            raise SyntaxError("grep: No parameters were given.")

        if len(parameters) == 1:
            parameters.append(constants.CURRENT_DIR)

        # processing flags
        recursive = False
        if 'recursive' in long_flags:
            recursive = True

        ignore_case = False
        if 'ignore_case' in long_flags:
            ignore_case = True

        # processing given regular expression
        regular_expression: re.Pattern[str] = self._process_regular_expression(
            parameters[0], ignore_case)

        # processing every given path
        output = []
        for path in parameters[1:]:
            original_path, path = self._normalize.normalize(
                path)
            try:
                # determine file type
                try:
                    is_file = os.path.isfile(path)
                    is_dir = os.path.isdir(path)
                except PermissionError:
                    self._logger.exception(
                        f"There is no permissions to access {path}.")
                    output.append(
                        f"grep: cannot find matchs in {original_path}. Permission denied.")
                    continue

                # check if path exists
                if not (is_file or is_dir):
                    self._logger.error(f"File {path} doesn't exists.")
                    output.append(
                        f"grep: File {original_path} can't be processed. It doesn't exist.")
                # try to process as file
                elif is_file:
                    output += (self._process_file(path,
                                                  original_path, regular_expression))
                # try to process as directory
                elif is_dir:
                    if recursive:
                        output += (self._process_directory(path,
                                                           original_path, regular_expression))
                    else:
                        self._logger.error(
                            f"Folder {path} can't be processed without recursive flag.")
                        output.append(
                            f"grep: folder {original_path} can't be processed without --recursive flag.")
            except PermissionError:
                self._logger.exception(
                    f"Cannot access {path}. Permission denied.")
                output.append(
                    f"grep: cannot find matches in {original_path}. Permission denied.")
        return "\n".join(output)


COMMAND_INFO = {
    "name": "grep",
    "function": lambda: Grep(Normalizer(), Helper()),
    "entry-point": "grep",
    "flags": ["recursive", "ignore_case", "help"],
    "aliases": {"r": "recursive", "i": "ignore_case"},
    "description": "Search."
}
