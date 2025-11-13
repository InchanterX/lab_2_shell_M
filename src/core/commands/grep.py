from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer
import logging
import re
import os
# import src.utils.constants


class grep:
    '''
    Command "grep" get regular expression and paths from the command
    and search by this regular expression in following files.
    Supports flag -r for recursive search and -i for registry independent search.
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logging.getLogger(__name__)

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
            self._logger.error("Not enough parameters was given.")
            raise SyntaxError("grep: Not enough parameters was given.")

        # processing flags
        recursive = False
        if 'recursive' in long_flags:
            recursive = True

        ignore_case = False
        if 'ignore_case' in long_flags:
            ignore_case = True

        # processing given regular expression
        regular_expression = parameters[0]
        regular_expression = _process_regular_expression(
            regular_expression, ignore_case)

        # processing every given path
        output = []
        for path in parameters[1:]:
            original_path, path = self._normalize.normalize(
                path)
            try:
                # if given path is invalid
                if not os.path.exists(path):
                    self._logger.error(f"File {path} doesn't exists.")
                    output.append(
                        f"grep: File {original_path} can't be processed. It doesn't exist.")
                # process files with given regular expression
                elif os.path.isfile(path):
                    output += _process_file(path,
                                            original_path, regular_expression)
            # if program failed to process file it is unaccessible
            except PermissionError:
                self._logger.exception(
                    f"There is no permissions to {path}.")
                output.append(
                    f"grep: cannot search in {original_path}. Permission denied.")

        def _process_regular_expression(regular_expression: str, ignore_case: bool) -> str:
            '''
            Get regular expression and use compile on ot for more convenient usage in future.
            If given expression is invalid function will return a error.
            '''
            try:
                if ignore_case == True:
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

        def _process_file(path: str, original_path: str, regular_expression: str) -> list[str]:
            '''
            Find all the matches in lines of given file
            and return them in numerated list of strings.
            '''
            try:
                output = []
                with open(path, "r", encoding="UTF-8", errors="ignore") as file:
                    for order, line in enumerate(file):
                        for match in regular_expression.finditer(line):
                            output.append(f"{file.name} {order} {match}")
            except PermissionError:
                self._logger.error(
                    f"Unable to open file {path}. Permission denied.")
                output.append(
                    f"grep: cannot search in {original_path}. Permission denied.")


COMMAND_INFO = {
    "name": "grep",
    "function": lambda: grep(Normalizer(), Helper()),
    "entry-point": "grep",
    "flags": ["recursive", "ignore_case", "help"],
    "aliases": {"r": "recursive", "i": "ignore_case"},
    "description": "Search."
}
