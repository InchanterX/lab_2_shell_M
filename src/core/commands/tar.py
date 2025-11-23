import os
import tarfile
from src.infrastructure.logger import logger
import src.infrastructure.constants as constants
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer


class Tar:
    """
    "Tar" command work with tar format of files. Make tar archives with .tar.gz extension.
    """

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logger

    def tar(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running tar with flags={long_flags}, parameters={parameters}"
        )

        # help call
        if "help" in long_flags:
            return self._helper.call_help("tar")

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("tar: No parameters were given.")

        # finding the best name for the archive
        archive_path = os.path.join(constants.CURRENT_DIR, "archive.tar.gz")
        archive_path = archive_path
        counter = 1
        while os.path.exists(archive_path):
            archive_path = os.path.join(
                constants.CURRENT_DIR, f"archive{counter}.tar.gz")
            counter += 1

        # processing parameters
        output = []
        with tarfile.open(archive_path, "w:gz") as my_tar:
            for parameter in parameters:
                original_path, path = self._normalize.normalize(parameter)
                if not os.path.exists(path):
                    self._logger.error(f"Path {path} is invalid.")
                    output.append(f"tar: {original_path} doesn't exist!")
                elif not os.access(path, os.R_OK):
                    self._logger.error(f"Path {path} is unaccessible.")
                    output.append(f"tar: Can't access {original_path}!")
                else:
                    try:
                        my_tar.add(path, arcname=os.path.basename(path))
                        self._logger.info(
                            f'Successfully added folder {path} to "{os.path.basename(archive_path)}".')
                        output.append(
                            f'Successfully added folder {original_path} to "{os.path.basename(archive_path)}"!')
                    except OSError:
                        self._logger.error(f"Unable to zip {path}.")
                        output.append(f"Unable to zip {original_path}!")

        return "\n".join(output)


COMMAND_INFO = {
    "name": "tar",
    "function": lambda: Tar(Normalizer(), Helper()),
    "entry-point": "tar",
    "flags": ["help"],
    "aliases": {},
    "description": "Tar given files.",
}
