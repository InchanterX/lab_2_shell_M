from src.infrastructure.logger import logger


class CommandLogger:
    '''
    Log the given command
    '''

    def __init__(self) -> None:
        self._logger = logger

    def log_command_call(self, command_name: str, long_flags: list[str], parameters: list[str]) -> None:
        '''
        Logging commands flags and parameters
        '''
        self._logger.debug(
            f"Running {command_name} with flags={long_flags}, parameters={parameters}")
