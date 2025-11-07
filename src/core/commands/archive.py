import os
import zipfile
import tarfile
import logging
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer


class Archive:
    '''
    "Archive"
    '''

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logging.getLogger(__name__)

    def zip(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running mv with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("mv")

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("mv: No parameters were given.")

        # processing parameters
        output = []
        for parameter in parameters:
            original_path, path = self._normalize.normalize(
                parameter)
            if not os.path.exists(path):
                self._logger.error(f"Path {path} is invalid.")
                output.append(f"zip: {original_path} doesn't exist!")
            if not os.access(path, os.R_OK):
                self._logger.error(f"Path {path} is unaccessible.")
                output.append(f"zip: Can't access {original_path}!")
            try:
                if file


COMMAND_INFO = {
    "name": "archive",
    "function": lambda: Archive(Normalizer(), Helper()),
    "entry-point": "archive",
    "flags": ["help"],
    "aliases": {},
    "description": "Display file content."
}
