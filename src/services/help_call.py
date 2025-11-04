import src.infrastructure.constants as constants
import logging


class Helper:
    '''

    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def call_help(self, command: str) -> list[str]:
        print(constants.REGISTRY[command])
        return 0
