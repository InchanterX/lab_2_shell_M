import os
import zipfile
from src.infrastructure.logger import logger
import src.infrastructure.constants as constants
from src.services.help_call import Helper
from src.services.path_normalizer import Normalizer


class Zip:
    """
    "Zip" files and folders to a zip archive.
    """

    def __init__(self, normalizer: Normalizer, helper: Helper) -> None:
        self._normalize = normalizer
        self._helper = helper
        self._logger = logger

    def zip(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running zip with flags={long_flags}, parameters={parameters}"
        )

        # help call
        if "help" in long_flags:
            return self._helper.call_help("zip")

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("zip: No parameters were given.")

        # finding the best name for the archive
        archive_path = os.path.join(constants.CURRENT_DIR, "archive.zip")
        archive_path = archive_path
        counter = 1
        while os.path.exists(archive_path):
            archive_path = os.path.join(
                constants.CURRENT_DIR, f"archive{counter}.zip")
            counter += 1

        # processing parameters
        output = []
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as my_zip:
            for parameter in parameters:
                original_path, path = self._normalize.normalize(parameter)
                if not os.path.exists(path):
                    self._logger.error(f"Path {path} is invalid.")
                    output.append(f"zip: {original_path} doesn't exist!")
                elif not os.access(path, os.R_OK):
                    self._logger.error(f"Path {path} is unaccessible.")
                    output.append(f"zip: Can't access {original_path}!")
                else:
                    try:
                        if os.path.isdir(path):
                            for root, dirs, files in os.walk(path):
                                for file in files:
                                    full_path = os.path.join(root, file)
                                    relative_path = os.path.relpath(
                                        full_path, os.path.join(path, "..")
                                    )
                                    my_zip.write(full_path, relative_path)
                            self._logger.info(
                                f'Successfully added folder {path} to "{os.path.basename(archive_path)}".')
                            output.append(
                                f'Successfully added folder {original_path} to "{os.path.basename(archive_path)}"!'
                            )
                        else:
                            file_name = os.path.basename(path)
                            my_zip.write(path, arcname=file_name)
                            self._logger.info(
                                f'Successfully added folder {path} to "{os.path.basename(archive_path)}".')
                            output.append(
                                f'Successfully added {original_path} to "{os.path.basename(archive_path)}"!'
                            )
                    except OSError:
                        self._logger.error(f"Unable to zip {path}.")
                        output.append(f"Unable to zip {original_path}!")

        return "\n".join(output)


COMMAND_INFO = {
    "name": "zip",
    "function": lambda: Zip(Normalizer(), Helper()),
    "entry-point": "zip",
    "flags": ["help"],
    "aliases": {},
    "description": "Zip given files.",
}
