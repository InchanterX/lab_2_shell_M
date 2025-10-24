# import src.utils.constants


class Example:
    '''
    Command "list"
    '''

    def __init__(self) -> None:
        pass

    def example(self) -> None:
        pass


COMMAND_INFO = {
    "name": "example",
    "flags": ["l", "a"],
    "description": "Do nothing.",
    "function": Example
}
