import src.utils.constants as constants
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

    def normalize(self, path: str) -> str:
        original_path = path

        # exclude extra '
        path = path.replace('\'', '')
        path = path.replace('\"', '')

        # unfolds, normalize and absolutize path
        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.join(constants.CURRENT_DIR, path)
        path = os.path.normpath(path)

        self._logger.debug(
            f"Converted path: {original_path} -> {path}")
        return path
