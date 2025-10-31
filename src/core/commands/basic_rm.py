import os
import shutil
import logging
from src.utils.path_normalizer import Normalizer


class Rm:
    '''
    Command "rm" takes lists of flags (--help, --recursive, --force or -r, -f) and parameters (>=1 file|folder paths) for deleting.
    Delete files if everything is write. Raise an exception in case of a error.
    Delete folders and all their content if there is [-r|--recursive] flag.
    If several parameters are given without --force will ask user's consent.
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def rm(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running rm with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            self._logger.info("Returned help string.")
            return 'rm [-r|--recursive|-f|--force|--help] [files|folders] - delete files and folders.'

        # no parameters were given
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError("rm: No parameters were given.")

        # processing flags
        force = False
        if 'force' in long_flags:
            force = True
        recursive = False
        if 'recursive' in long_flags:
            recursive = True

        # processing removing of files and folders
        output = []
        for parameter in parameters:
            original_parameter = parameter
            parameter = Normalizer().normalize(parameter)

            # prohibited path is given
            if parameter in ("/", os.path.abspath("..")):
                self._logger.exception(
                    f"You can't delete {parameter}.")
                output.append(
                    f"rm: you can't delete {original_parameter}.")

            # file was given
            elif os.path.isfile(parameter):
                try:
                    # delete file
                    os.remove(parameter)
                    self._logger.debug(
                        f"Deleted file {parameter}.")
                except PermissionError:
                    self._logger.exception(
                        f"There is no permissions to delete {parameter}.")
                    output.append(
                        f"rm: cannot delete {original_parameter}. Permission denied.")
                except OSError as e:
                    self._logger.exception(
                        f"Failed to delete {parameter}: {e}")
                    output.append(
                        f"rm: failed to delete {original_parameter}.")

            # folder was given
            elif os.path.isdir(parameter):

                # check if folder is empty
                folder_is_empty = False
                if len(os.listdir(parameter)) == 0:
                    folder_is_empty = True

                # ask for a consent to delete a folder
                consent = 0
                if not force and not folder_is_empty:
                    answer = input(
                        f"rm: remove {original_parameter}? [y/N]\n").strip().lower()
                    if answer in {"y", "yes"}:
                        consent = 1
                        self._logger.info(
                            f"User gave it\'s consent for deleting folder {parameter}")
                    else:
                        self._logger.info(
                            f"User rejected from deleting folder {parameter}")

                # delete the folder if there is one (or more) permission
                if force or consent or recursive or folder_is_empty:
                    try:
                        shutil.rmtree(parameter)
                        self._logger.debug(
                            f"Successfully deleted folder {parameter}.")
                    except PermissionError:
                        self._logger.exception(
                            f"There is no permissions to delete {parameter}.")
                        output.append(
                            f"rm: cannot delete {original_parameter}. Permission denied.")
                    except OSError as e:
                        self._logger.exception(
                            f"Failed to delete {parameter}: {e}")
                        output.append(
                            f"rm: failed to delete {original_parameter}.")

                # consent wasn't given
                else:
                    self._logger.warning(
                        f"Unable to delete folder {parameter} without a consent or/and recursive flag.")
                    output.append(
                        f"rm: you can't remove the folder {original_parameter} without consent or flag [-r|--recursive].")

            # invalid file was given
            else:
                self._logger.error(f"Path not found: {parameter}")
                output.append(
                    f"rm: failed to delete {original_parameter}. It doesn't exist.")

        self._logger.info("Rm successfully deleted all valid files.")
        return "\n".join(output)


COMMAND_INFO = {
    "name": "rm",
    "function": Rm,
    "entry-point": "rm",
    "flags": ["recursive", "force" "help"],
    "aliases": {"r": "recursive", "f": "force"},
    "description": "Copy files to a different folder."
}
