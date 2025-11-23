from src.infrastructure.logger import logger
import src.infrastructure.constants as constants
from src.services.help_call import Helper
from src.services.command_logger import CommandLogger


class Pwd:
    '''
    Command "pwd" returns current directory
    '''

    def __init__(self, helper: Helper, command_logger: CommandLogger) -> None:
        self._helper = helper
        self._command_logger = command_logger
        self._logger = logger

    def pwd(self, long_flags: list[str], parameters: list[str]) -> str:
        self._command_logger.log_command_call("pwd", long_flags, parameters)

        # help call
        if 'help' in long_flags:
            return self._helper.call_help("pwd")

        return constants.CURRENT_DIR


COMMAND_INFO = {
    "name": "pwd",
    "function": lambda: Pwd(Helper(), CommandLogger()),
    "entry-point": "pwd",
    "flags": ["help"],
    "aliases": {},
    "description": "Returns current directory."
}
