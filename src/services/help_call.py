import src.infrastructure.constants as constants
import logging


class Helper:
    '''
    Returns help message to the console with data that given in the command config
    '''

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def call_help(self, command: str) -> list[str]:
        # It is better to add check for given name existence
        name = constants.REGISTRY[command]["name"]
        # It is better to check if elements are not empty, if they are empty it's better not to add them to the output
        flags = constants.REGISTRY[command]["flags"]
        aliases = constants.REGISTRY[command]["aliases"]
        description = constants.REGISTRY[command]["description"]
        flags_str = "\n".join(f"--{flag}" for flag in flags)
        aliases_str = " ".join(f"-{alias}" for alias in aliases)
        result = f"Command {name}.\n{description}\nSupports {len(flags)} flags:\n{flags_str}\nSupports {len(aliases)} aliases\n{aliases_str}"
        self._logger.info("Returned help string.")
        return result
