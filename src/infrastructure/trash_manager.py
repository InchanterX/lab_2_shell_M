import os
import shutil
import logging
import src.infrastructure.constants as constants
from src.services.path_normalizer import Normalizer


class TrashManager:
    '''
    "TrashManager" makes backups for files that will be edited during execution of commands rm, mv and cp that can be undone.
    And provide a function to restore them.
    '''

    def __init__(self) -> None:
        self._normalize = Normalizer()
        self._logger = logging.getLogger(__name__)
        if not os.path.exists(constants.TRASH_DIR):
            os.makedirs(constants.TRASH_DIR, exist_ok=True)

    def _history_dir(self, history_id: int) -> str:
        '''
        Get dir path for given ID
        '''
        return os.path.join(constants.TRASH_DIR, str(history_id))

    def _is_prohibited_path(self, path: str) -> bool:
        '''
        Check if path is prohibited from being backed up, preventing recursive backups
        '''

        if path == "/":
            return True

        # Windows crutch
        if os.name == "nt":
            normalized = os.path.normpath(path)
            drive, rest = os.path.splitdrive(normalized)
            if drive and (not rest or rest == "\\"):
                return True

        # check parent dir
        abs_parent = os.path.abspath("..")
        if path == abs_parent:
            return True

        return False

    def create_backup(self, history_id: int, command_name: str, parameters: list[str]) -> str | None:
        '''
        Create backup of all valid files from parameers that need to be backuped.
        Backup files in 3 scenarioes - rm, mv or cp commands.
        '''
        backup_dir = self._history_dir(history_id)

        # Create backup directory
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)

        backup_paths = []
        # rm command case - backup all files that will be deleted
        if command_name == "rm":
            for parameter in parameters:
                original_parameter, normalized_parameter = self._normalize.normalize(
                    parameter)
                # skip prohibited paths
                if self._is_prohibited_path(normalized_parameter):
                    self._logger.warning(
                        f"Skipping backup of prohibited path: {normalized_parameter}")
                    continue
                if os.path.exists(normalized_parameter):
                    backup_path = os.path.join(
                        backup_dir, os.path.basename(normalized_parameter))
                    try:
                        if os.path.isfile(normalized_parameter):
                            shutil.copy2(normalized_parameter, backup_path)
                        elif os.path.isdir(normalized_parameter):
                            shutil.copytree(normalized_parameter,
                                            backup_path, dirs_exist_ok=True)
                        backup_paths.append(backup_path)
                        self._logger.debug(
                            f"Made a backup of {normalized_parameter} to {backup_path}")
                    except Exception as e:
                        self._logger.exception(
                            f"Failed to backup {normalized_parameter}: {e}")

        # mv command case - backup moving files
        elif command_name == "mv":
            # make a backup if mv doesn't work in renaming mode
            if len(parameters) >= 2:
                for parameter in parameters[:-1]:
                    original_parameter, normalized_parameter = self._normalize.normalize(
                        parameter)
                    # skip prohibited paths
                    if self._is_prohibited_path(normalized_parameter):
                        self._logger.warning(
                            f"Skipping backup of prohibited path: {normalized_parameter}")
                        continue
                    if os.path.exists(normalized_parameter):
                        backup_path = os.path.join(
                            backup_dir, os.path.basename(normalized_parameter))
                        try:
                            if os.path.isfile(normalized_parameter):
                                shutil.copy2(normalized_parameter, backup_path)
                            elif os.path.isdir(normalized_parameter):
                                shutil.copytree(
                                    normalized_parameter, backup_path, dirs_exist_ok=True)
                            backup_paths.append(backup_path)
                            self._logger.debug(
                                f"Made a backup of {normalized_parameter} to {backup_path}")
                        except Exception as e:
                            self._logger.exception(
                                f"Failed to backup {normalized_parameter}: {e}")

        # cp command case
        # How many nesting lines we need? Yes.
        elif command_name == "cp":
            if len(parameters) >= 2:
                target_dir = parameters[-1]
                original_target, normalized_target = self._normalize.normalize(
                    target_dir)
                if os.path.isdir(normalized_target):
                    for parameter in parameters[:-1]:
                        original_parameter, normalized_parameter = self._normalize.normalize(
                            parameter)
                        if os.path.exists(normalized_parameter):
                            moving_file = os.path.join(
                                normalized_target, os.path.basename(normalized_parameter))
                            if os.path.exists(moving_file):
                                backup_path = os.path.join(
                                    backup_dir, os.path.basename(normalized_parameter))
                                try:
                                    if os.path.isfile(moving_file):
                                        shutil.copy2(moving_file, backup_path)
                                    elif os.path.isdir(moving_file):
                                        shutil.copytree(
                                            moving_file, backup_path, dirs_exist_ok=True)
                                    backup_paths.append(backup_path)
                                    self._logger.debug(
                                        f"Made a backup of {moving_file} to {backup_path}")
                                except Exception as e:
                                    self._logger.exception(
                                        f"Failed to backup {moving_file}: {e}")

        if backup_paths:
            return backup_dir
        return None

    def restore_backup(self, history_id: int, command_name: str, parameters: list[str]) -> bool:
        '''
        Restore file from the .trash by it's data. Returns True/False as a result of work.
        '''
        backup_dir = self._history_dir(history_id)

        if not os.path.exists(backup_dir):
            self._logger.warning(
                f"Backup directory {backup_dir} does not exist!")
            return False

        try:
            # rm command case
            if command_name == "rm":
                # restore files to the original locations
                for parameter in parameters:
                    original_parameter, normalized_parameter = self._normalize.normalize(
                        parameter)
                    backup_path = os.path.join(
                        backup_dir, os.path.basename(normalized_parameter))

                    if os.path.exists(backup_path):
                        if os.path.isfile(backup_path):
                            shutil.copy2(backup_path, normalized_parameter)
                        elif os.path.isdir(backup_path):
                            if os.path.exists(normalized_parameter):
                                shutil.rmtree(normalized_parameter)
                            shutil.copytree(
                                backup_path, normalized_parameter, dirs_exist_ok=True)
                        self._logger.debug(
                            f"Succesfully restored {backup_path} to {normalized_parameter}")

            # mv command case
            elif command_name == "mv":
                # restore source files in their original locations
                if len(parameters) >= 2:
                    target_parameter = parameters[-1]
                    original_target, normalized_target = self._normalize.normalize(
                        target_parameter)

                    for parameter in parameters[:-1]:
                        original_parameter, normalized_parameter = self._normalize.normalize(
                            parameter)
                        backup_path = os.path.join(
                            backup_dir, os.path.basename(normalized_parameter))

                        if os.path.exists(backup_path):
                            if os.path.isfile(backup_path):
                                shutil.copy2(backup_path, normalized_parameter)
                            elif os.path.isdir(backup_path):
                                if os.path.exists(normalized_parameter):
                                    shutil.rmtree(normalized_parameter)
                                shutil.copytree(
                                    backup_path, normalized_parameter, dirs_exist_ok=True)
                            self._logger.debug(
                                f"Succesfully restored {backup_path} to {normalized_parameter}")

                            # Remove file that was created by moving
                            moved_path = os.path.join(
                                normalized_target, os.path.basename(normalized_parameter))
                            if os.path.exists(moved_path):
                                if os.path.isfile(moved_path):
                                    os.remove(moved_path)
                                elif os.path.isdir(moved_path):
                                    shutil.rmtree(moved_path)

            # cp command case - remove copied files
            elif command_name == "cp":
                if len(parameters) >= 2:
                    target_parameter = parameters[-1]
                    original_target, normalized_target = self._normalize.normalize(
                        target_parameter)

                    for parameter in parameters[:-1]:
                        original_parameter, normalized_parameter = self._normalize.normalize(
                            parameter)
                        copy_path = os.path.join(
                            normalized_target, os.path.basename(normalized_parameter))

                        if os.path.exists(copy_path):
                            backup_path = os.path.join(
                                backup_dir, os.path.basename(normalized_parameter))

                            # Restore a file and just delete copy
                            if os.path.exists(backup_path):
                                if os.path.isfile(copy_path):
                                    shutil.copy2(backup_path, copy_path)
                                elif os.path.isdir(copy_path):
                                    shutil.rmtree(copy_path)
                                    shutil.copytree(
                                        backup_path, copy_path, dirs_exist_ok=True)
                                self._logger.debug(
                                    f"Succesfully restored {backup_path} to {copy_path}")
                            # In case backup wasn't found
                            else:
                                if os.path.isfile(copy_path):
                                    os.remove(copy_path)
                                elif os.path.isdir(copy_path):
                                    shutil.rmtree(copy_path)
                                self._logger.debug(f"Removed {copy_path}")

            return True
        except Exception as e:
            self._logger.exception(
                f"Failed to restore backup of {backup_dir}: {e}")
            return False

    def delete_backup(self, history_id: int) -> None:
        '''
        Delete backup dir for given ID
        '''
        backup_dir = self._history_dir(history_id)
        if os.path.exists(backup_dir):
            try:
                shutil.rmtree(backup_dir)
                self._logger.debug(
                    f"Successfully deleted backup directory {backup_dir}")
            except Exception as e:
                self._logger.exception(
                    f"Failed to delete backup {backup_dir}: {e}")
