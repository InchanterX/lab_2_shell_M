from src.infrastructure.logger import logger


class ParameterValidator:
    '''
    Validates command for having right amount of parameters
    '''

    def __init__(self) -> None:
        self._logger = logger

    def validate_no_parameters(self, parameters: list[str], command_name: str) -> None:
        '''
        Raise SyntaxError if parameters list is empty
        '''
        if parameters == []:
            self._logger.error("No parameters were given.")
            raise SyntaxError(f"{command_name}: No parameters were given.")

    def validate_not_enough_parameters(self, parameters: list[str], min_count: int, command_name: str) -> None:
        '''
        Raise SyntaxError if command received not enough parameters
        '''
        if len(parameters) < min_count:
            self._logger.error("Not enough parameters were given.")
            raise SyntaxError(
                f"{command_name}: Not enough parameters were given.")
