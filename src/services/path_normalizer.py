import src.infrastructure.constants as constants
from src.infrastructure.logger import logger
import os


class Normalizer:
    '''
    Normalize given path by excluding escaping ', unfolding ~, .. and . with values.
    Then it create an absolute version of path and normalize it.
    Returns absolute normalized path.
    '''

    def __init__(self) -> None:
        self._logger = logger

    def normalize(self, path: str) -> tuple[str, str]:
        original_path = path

        # exclude extra ' and "
        normalized_path = path.replace('\'', '')
        normalized_path = normalized_path.replace('\"', '')

        # unfolds, normalize and absolutize path
        normalized_path = os.path.expanduser(normalized_path)
        if not os.path.isabs(normalized_path):
            normalized_path = os.path.join(
                constants.CURRENT_DIR, normalized_path)
        normalized_path = os.path.normpath(normalized_path)

        self._logger.debug(
            f"Converted path: {original_path} -> {normalized_path}")
        return original_path, normalized_path
