import logging
import src.infrastructure.constants as constants
from src.services.help_call import Helper


class Pwd:
    '''
    Command "pwd" returns current directory
    '''

    def __init__(self, helper: Helper) -> None:
        self._helper = helper
        self._logger = logging.getLogger(__name__)

    def pwd(self, long_flags: list[str], parameters: list[str]) -> str:
        self._logger.debug(
            f"Running pwd with flags={long_flags}, parameters={parameters}")

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("pwd")

        return constants.CURRENT_DIR


COMMAND_INFO = {
    "name": "pwd",
    "function": lambda: Pwd(Helper()),
    "entry-point": "pwd",
    "flags": ["help"],
    "aliases": {},
    "description": "Returns current directory."
}
