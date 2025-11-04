import src.infrastructure.constants as constants
import logging
import os


class Normalizer:
    '''
    Normalize given path by excluding escaping ', unfolding ~, .. and . with values.
    Then it create an absolute version of path and normalize it.
    Returns absolute normalized path.
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def normalize(self, path: str) -> list[str]:
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
